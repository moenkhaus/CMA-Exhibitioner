import requests
import pymongo

class exhibitioner:

    api_base_url = "https://openaccess-api.clevelandart.org/api/"
    db_collection_name = "mini_exhibit"
    db_connection_string = None
    exhibits = [] # main exhibits view to explore
    mini_exhibit_art = [] # collection of art tagged for a mini exhibit
    ref_art = [] # local view of art data obtained either through viewing an exhibit or searching
    ref_exhibit = None # optionally used for reference data for mini exhibit
    ref_search = None # optionally used for reference data for mini exhibit

    def __init__(self,connection_string):
        self.db_connection_string = connection_string
        
    def view_exhibits(self,page=0):
        base_url = self.api_base_url+"exhibitions"
        params = {
            "skip": 100*page
        }
        self.exhibits = requests.get(base_url, params=params).json()["data"]
        for id, exhibit in enumerate(self.exhibits, start=0):
            numArtworks = len(exhibit['artworks'])
            if (numArtworks > 7):
                print(f"{id} : {exhibit['title']} ({numArtworks})")

    def print_art(self,index,art):
        print(f"'index' : {index}")
        print(f"'accession_number' : {art['accession_number']}")
        print(f"'title' : {art['title']}")
        print(f"'tombstone' : {art['tombstone']}")
        print(f"'url' : {art['url']}")

    def view_exhibit(self,id):
        self.ref_exhibit = self.exhibits[id]
        print(f"Viewing {self.ref_exhibit['title']}")
        self.ref_art = self.ref_exhibit['artworks']
        for i, art in enumerate(self.ref_art, start=0):
            self.print_art(i,art)

    def search_art(self,search,page=0):
        self.ref_search = search
        print(f"Searching {self.ref_search}")
        base_url = self.api_base_url+"artworks"
        params = {
            "q": search,
            "limit": 10,
            "skip" : 10*page
        }
        self.ref_art = requests.get(base_url, params=params).json()['data']
        for i, art in enumerate(self.ref_art, start=0):
            self.print_art(i,art)

    def add_art(self,id):
        if not any (self.ref_art):
            print("Find art before attempting to add via 'exhibit' or 'search' commands")
            return
        art = self.ref_art[id]
        if not hasattr(art, "athena_id"): # cannot use cached version when viewing exhibition ref data and not viewing full art search api
            base_url = self.api_base_url + "artworks/" + art['accession_number']
            art = requests.get(base_url).json()['data']
        self.mini_exhibit_art.append(art)

    def push_mini_exhibit(self,name):
        if not any (self.mini_exhibit_art):
            print("Find art before attempting to add via 'exhibit' or 'search' commands")
            return
        print(f"Pushing {name}")
        client = pymongo.MongoClient(self.db_connection_string)
        db = client["cmoa"]
        collection = db[self.db_collection_name]
        artToPost = []
        for art in self.mini_exhibit_art:
            a = {
                'athena_id': art['athena_id'],
                'accession_number': art['accession_number'],
                'tombstone': art['tombstone'],
                'ref_search': self.ref_search,
                'name': name,
            }
            if self.ref_exhibit is not None:
                a['ref_exhibitid'] = self.ref_exhibit['id']
            if 'web' in art['images']:
                a['image'] = art['images']['web']['url']
            elif 'full' in art['images']:
                a['image'] = art['images']['full']['url']
            artToPost.append(a)
        inserted_ids = collection.insert_many(artToPost).inserted_ids
        print(f"Data inserted successfully with IDs: {inserted_ids}")

    def pull_mini_exhibit(self,name):
        print(f"Pulling {name}")
        client = pymongo.MongoClient(self.db_connection_string)
        db = client["cmoa"]
        collection = db[self.db_collection_name]
        query = {"name": name}
        result = collection.find(query)
        for art in result:
            print(art)

    def wipe(self):
        self.ref_art = []
        self.ref_exhibit = None
        self.ref_search = None
        self.exhibits = []
        self.mini_exhibit_art = []

def main():
    # normally the connection auth would be passed in at runtime from a secure source such as an environment variable or key vault
    connection_string = "mongodb+srv://demouser:demopw@cluster0.m7swswc.mongodb.net/?retryWrites=true&w=majority"
    e = exhibitioner(connection_string) 
    e.view_exhibits(0)
    while True:
        command = input("Enter a command: exhibits {page}, exhibit {index}, search {phrase}, searchpage {page} {phrase}, add {index}, push {name}, pull {name}, wipe, quit \n")
        if command.startswith('exhibits'):
            c, page, = command.split(' ')
            page = int(page)
            e.view_exhibits(page)
        elif command.startswith('exhibit'):
            c, id = command.split(' ')
            e.view_exhibit(int(id))
        elif command.startswith('searchpage'):
            _, searchPage, searchQuery = command.split(' ', 2)
            e.search_art(searchQuery, int(searchPage))
        elif command.startswith('search'):
            _, searchQuery = command.split(' ',1)
            e.search_art(searchQuery,0)
        elif command.startswith('add'):
            _, id = command.split(' ')
            e.add_art(int(id))
        elif command.startswith('push'):
            _, name = command.split(' ',1)
            e.push_mini_exhibit(name)
        elif command.startswith('pull'):
            _, name = command.split(' ',1)
            e.pull_mini_exhibit(name)
        elif command.startswith('wipe'):
            e.wipe()
        elif command.startswith('quit'):
            return
        else:
            print("error: invalid command")

if __name__ == "__main__":
    main()