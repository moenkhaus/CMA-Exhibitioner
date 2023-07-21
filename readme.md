# App

The CMA Exhibitioner is a Python app that enables users to explore exhibitions, related artwork, perform searches for related content, and curate lists of artwork for mini exhibits that can be persisted online and accessed later.

## Setup

- Ensure you have Python 3.10+ installed and the standard pip package installer.
- Install package dependencies:
    - pip install requests
    - pip install pymongo
- Run the exhibit.py Python script (on Windows, use "python .\exhibit.py").
- See the example section below for a typical command execution path.
- Upon running, it displays the first page of exhibits and prompts for a command to begin exploration.
- To use the push and pull commands, the user must have their IP address added to the MongoDB access list. Please - contact me directly for access.

## Commands

- exhibits {page}: Lists out exhibits, 100 items at a time, showing only those with 8 or more artworks.
- exhibit {index}: Lists out a specific exhibit with related artwork.
- search {phrase}: Searches the art API using the provided phrase, displaying 10 items at a time.
- searchpage {page} {phrase}: Similar to the search command but with the ability to page through the results.
- add {index}: Adds art based on the index from either the exhibit or search results listing.
- push {name}: Pushes the mini exhibit to persistence, including the added artwork, with the given name for future access.
- pull {name}: Pulls the mini exhibit from persistence based on the provided name.
- wipe: Wipes out local data, useful for setting up a second mini exhibit.
- quit: Exits the app.

## Example
- python .\exhibit.py
- exhibit 93 
- add 1
- add 18
- search scotia
- add 3
- push scotia mountains
- pull scotia mountains
- quit

## Comments
- Exhibit and search data are optionally persisted for reference.
- Error handling for commands is not currently implemented.
- The connection string is hard-coded and requires improved security handling.

# Exercise Questions

*How did you approach this problem and why you end up with the solution you did?*

Understanding the api endpoints and data model were key components to understanding the problem space. Seeing that simple api interactions were involved I quickly went to pinging an endpoint to validate access. After having something up and running I created an interactive terminal experience to allow exploring the content and dynamically be able to add art to my mini exhibit as I went. After some basic refactoring and encapsulation I created a reusable component for use in either frontend or backend apps. There were no major requirements listed out so I kept the solution straightforward and stuck with designing dynamic actions that the user drives without any terminal interuption.

*How long did it take you to complete?*

Creating the api calls to query the data needed and integrate with MongoDB took less than an hour. Wiring it all together in a cohesive app took a few more hours to have a designed user experience intended for common use and committing to git.

*How would you change your solution in order to scale it up to a web application where users can select an exhibition, highlight and similarity criteria, and receive results?*

I would use a standard web framework solution for my runtime utilizing any existing solutions made available within the organization. From a scalability standpoint, I would take a look at existing user loads to anticipate load time needs. I might invest time into architecting a load test solution and designing a horizontally scalable runtime. I would work towards wrapping the primary class created to be used via a frontend API and start thinking through validating user input and enhancing the user experience such as better paging or advanced searching. A clear difference from a terminal to a web app is the ability to view images and in general using the various HTML elements. With this in mind, I would mock out the user flow and create web component designs through mockups or quick prototyping work. There are some missing features needed to support a web app so exploring them fully would also be top of mind. When I think of scale, it is not just for handling performance requirements but also the demands of the user experience. Prodiminetly I would look to understand and vet the requirements further starting with who the intended users are and why they need or want such a system. For instance, the system is quite different if it is intended for use by an internal intranet for CMA to post to social media versus general consumption where users are required to be a registered CMA member and logged in to share with friends or use for other personal use cases. Alternatively, non-CMA users might just only have read-only access to the mini exhibitions, again throwing up more questions to the design and structural requirements of the system. Having a better understanding of the existing landscape and having vetted out the requirements I would begin down a path of spending development cycles to deliver a solution proving the scalability through kpis over time and justify continued operation and investment. There are a mutltitude of things to consider when building a web app and having a standard development framework in place would be critical for the longevity of the application adding to the bucket of work plenty of NFR such as observability and analytics.

*How would you set this up as a process that runs daily, with different results, and posts them to social media platforms via API?*

I would use a standard backend job runner to run and produce the results. The trick would be determining what the criteria is for having a social media postable content that is approvable by the human staff at CMA. Using randomization, I could begin showing a proof of concept of the system producing various outputs for review. Before any of this work, I would start from a discovery standpoint to fully understand and vet out the request for the system. Since we are managing social media account information I would ensure the proper security measures are in place and the proper folks were consulted before using any of these platforms. In general, I would target producing a large set of procedurally generated content based on trial and error to queue up hundreds of variations based on simple keywords like "moon" or "woman" that I know contain results and create mini landing pages for the social media posts to land on. With the expansion of AI-assisted toolchains like ChatGPT, I would consider looking at procedurally creating more content and permutations. In the end I think any such system would always need human approval and I would redesign the system to be queue based with human approval required and line up the posts ahead of time. This would allow a human to review the content strategy and be able to make adjustments to the system. Knowing what has been posted or not already would also be a part of this social media content strategy system and I would make use of historical record keeping to eliminate duplicates and focus on generating fresh relevant content. Sometimes the biggest challenge is not creating the system, but designing the right one.