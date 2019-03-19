# To Do List

- [ ] Daniel is going to set up Django project
- [ ] Chinh is going to set up Postgres
- [ ] Chinh is going to set up gitignore and other basics
- [ ] Everyone will think about models
- [x] Anna will clean up feature branch mess


# Decisions

Our app is called core
Our settings folder is called apile
We are going to extend the existing user model
Our theme - support people who advocate for homeless

# Models

User, but called something different. Submitters, because they submit comments, links, votes.

Post
 * URL,
 * slug, 
 * date_added, 
 * submitter, 
 * title, 
 * description
 
Comment 
 * (comments on posts), 
 * text, 
 * datetime_added, 
 * (created by) submitter,  
 
Vote - 
 * (comments on posts), 
 * datetime_added, 
 * (created by) submitter,  


