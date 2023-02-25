# udplatforms_CRUD
Flask API to demonstrate one - to -many relationship
### Features
This project has demonstrated parent-child relationship with respective fields such as: 
**Parent** table has **firstname, lastname, street, city, state, zip code** where **Child** table has **only name** without address.

Here the database(**SQLALCHEMY**) model has ben designed based on **one-to-many** parent-child relationship as single parent may have multiple children, however, every children belongs to one parent
:tw-1f600: 
### Tools used
- python (3.7.6) Windows Version
- Flask (2.2.2)
- Werkzeug (2.2.2)
- Flask SQLAlchemy (2.0.3)
