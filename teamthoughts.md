# To Do List for MONDAY

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

**Post
 * URL,
 * slug, 
 * date_added, 
 * poster (which is a submitter,) 
 * title, 
 * description
 * (voted_as vote) ManytoMany to vote
 * (commented_as comment) ManytoMany on comment
 
**Comment 
 * (comments on posts), 
 * text, 
 * datetime_added, 
 * (created by) commentor (which is a submitter,  
 
**Vote - 
 * (comments on posts), 
 * datetime_added, 
 * (created by) voter (which is a submitter),  


# To Do List for TUESDAY EARLY

- [ ] Daniel is going to do registration redux
- [ ] Chinh is going to do models.py
- [ ] Anna is going to get dummy data.

