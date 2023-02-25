# udplatforms_CRUD
Flask API to demonstrate one - to -many relationship
### Features
This project has demonstrated parent-child relationship with respective fields such as: 
**Parent** table has **firstname, lastname, street, city, state, zip code** where **Child** table has **only name** without address.

Here the database(**SQLALCHEMY**) model has ben designed based on **one-to-many** parent-child relationship as single parent may have multiple children, however, every children belongs to one parent

### Tools used
- python (3.7.6) Windows Version
- Flask (2.2.2)
- Werkzeug (2.2.2)
- Flask SQLAlchemy (2.0.3)
### To understand better, here is the flow diagram of the endpoints
(https://github.com/NazminJuli/udplatforms_CRUD/blob/b576fd91789ed2281d8c8e71e02d82061df1b01f/API%20flow%20chart.png)
- Home page URL (localhost:5000/)
   - For simplicity, I have used parent's naming detail as  unique constraints
   - each parent may have childern or not
   - each child must belong to a parent
   *UPDATE* and *DELETE*  (cascade enabled, while removing parent, all details including child will be removed) has been implemented for address and parent respectively.
- Search page URL (localhost:5000/search)
