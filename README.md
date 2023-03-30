# CYBERQUARIUM
Jovian Lim <lizh22gm@student.ju.se> <br>
Jie Chung Ong <onji22ug@student.ju.se> <br>
A Project Work in Web Development – Advanced Concepts
Jönköping University 2023

## Table of Contents
<ul>
    <li> <a href="#intro"> Introduction </a> </li>
    <li> <a href="#gui"> Graphical User Interface </a> </li>
    <li> <a href="#arch"> Architecture </a> </li>
    <li> <a href="#api"> REST API </a> </li>
    <li> <a href="#frontend"> Frontend </a> </li>
    <li> <a href="#db"> Database </a> </li>
    <li> <a href="#backend"> Backend </a> </li>
    <li> <a href="#worklog"> Worklog </a> </li>
</ul>

## Introduction {#intro}

CyberQuarium is a web application that enables users to hatch and breed virtual animals. The platform
was created as a fun and interactive way for users to engage with virtual pets and experiment with
breeding different species. Users can login, register, and sign in using their Google accounts. Once signed
in, they can buy eggs, hatch them, and breed their animals to create new hybrids.

The platform can be used as a form of entertainment and education. It allows users to learn about
animal breeding in a fun and interactive way. Users can also connect with others who share similar
interests and exchange tips and advice on breeding for their virtual animals, or even buy and sell their
virtual eggs and animals on the CyberQuarium marketplace, creating an environment where users are
able to learn about the basic of economics, including the law of supply and demand.

Anyone who enjoys virtual pets, animal breeding, or interactive games would find this platform engaging
and enjoyable. The platform is designed for all age groups and can be used by anyone who has an
interest in virtual animals.

Users can access the platform through their web browser. Once they sign in, they can navigate through
the platform using the frontend application and interact with the virtual animals through the REST API.

Figure 1 : UML use case diagram of CyberQuarium
Graphical User Interface

Upon accessing the CyberQuarium web application platform, users will first be presented with a landing
page.

Figure 1: Landing Page

Users can login or register using their email and password, or they can use their Google account to sign
in.

Figure 2a: Login Page

Figure 2b: Registration Page

Figure 2c: Sign-in with Google popup

After logging in, users are presented with the Home Page, where users can see their coins balance (at the
top right corner) and a “welcome back! (username)” message. From the home page, users can be routed
to the Market Page and Inventory Page with two separate buttons below. Users can also access the
Navigation Bar (by clicking on the CyberQuarium Logo at the top left corner), to access the Home Page,
Market Page and Inventory Page, or to Logout.

Figure 3a: Home Page

Figure 3b: Home Page with NavBar

When the user is routed to the Market Page, the user will be able to view a default listing of an egg being
sold for 20 coins and is able to buy the egg with the “Buy Egg” button. The User will also be able to view
other Market Listings that have been listed by other Users for sale (Both Eggs and Animals can be listed
for sale in the Market Page).

Figure 4: Market Page

In the Inventory Page, users will be able to view all the Eggs and Animals that the user owns. For an Egg,
users can view the rarity and price of the egg or choose to either List the Egg on Market or to Hatch it by
using the respective buttons within the Egg card. For an Animal, users can view the rarity, species, name,
coin yield and coins yielded (since DOB) or choose to Burn, List the Animal on Market or to view
information regarding the Animal using the respective buttons in the Animal card. Users can also click on
the “Refresh Yields” button on the bottom of the page to ping the server to refresh the coins yields of
every animal. If the user wishes to breed two different Animals, the user can click on both Animal cards
and the “Breed” button will appear at the bottom of the page. Once the Animals have been bred, the
hybrid Animal (child) will appear as an Animal card.

Figure 5a: Inventory Page (Egg)

Figure 5b: Breeding Animals

When the user clicks on the “Info” button of an Animal, the user will be routed to the Animal Page,
where the Date of Birth, Rarity, Species, Name, Coin Yield, Coins Yielded and Owner of the Animal will be
displayed. Users will click on “Back to Inventory” button at the bottom of the page to return to the
Inventory Page

Figure 6 a: Animal Page

Users can list their eggs or animals on the market place by clicking on List on Market, a card will be
displayed for the user to input the listing name and listing price.

Figure 6b: Market Listing Card

Figure 6c: Market Page Listing

Architecture

The CyberQuarium platform consists of three main components: frontend, backend, and database. The
frontend is built using the Svelte single-page application framework, while the backend is built using the
Flask web framework. The database used is MySQL.

The frontend and backend components are deployed separately and communicate with each other
through the REST API. The frontend application is served to the end-users through their web browser.
The backend server runs on a separate container and provides the necessary REST endpoints for the
frontend to interact with the database.

The entire platform is containerized using Docker. The frontend and backend each run in separate
containers. The containers are managed using Docker Compose.
Figure 7 : Architecture of CyberQuarium
REST API

The CyberQuarium platform exposes a REST API that allows users to interact with the different resources
available on the platform. The API supports the following operations:

GET: Retrieves information about a resource

POST: Creates a new resource

The REST API endpoints that are supported by the CyberQuarium platform are listed below:

Register: POST /register

This endpoint is used to register a new user on the platform. The user should provide their email,
‘confirm’ email and password in the request body. The server then checks if the email is in a valid email
format and whether the password is strong enough (at least 8 characters, with uppercase, lowercase,
digit, and special character). If the email matches the ‘confirm’ email and the email is not already
registered, the server will hash the user’s password and create a new user in the database. A new
session id will also be generated for the user and stored in the database. The server will then return a
"User registered successfully" message.

Login: POST /login

This endpoint is used to authenticate a user and obtain an access token. The user should provide their
email and password in the request body. Server will then check if user exists in the database and
password matches. If the credentials are correct, the server generate a new session id for the user and
stored in the database. The server will then return a "User logged in successfully" message, along with
the session id.

Google Login: POST /google

This endpoint is used to authenticate a user using their Google account. The user should be redirected to
this endpoint to authorize the application. If the credentials are correct, the server generate a new
session id for the user and stored in the database. The server will then return a "User logged in
successfully" message, along with the session id.

Logout: POST /logout

This endpoint is used to log a user out of the current session. If user is found in the User database, user’s
session id will be set to None and the server will return a logout successful message.

Check Session: POST /api/session

This endpoint is used to receive a username and session id and checks if the session is valid. An error
message is returned if session id is None, or user does not exist in the database.

Get User Profile: GET /api/user/

This endpoint is used to retrieve information about a user. The user ID should be provided in the URL
parameter. If the user exists on the database, the server will return a JSON object containing the user's
id, username, email and coins. If the user does not exist on the database, the server will return an error
message.

Create Egg: POST /api/create_egg

This endpoint is used to create an egg, when called, this endpoint will initialize a Egg Class from the
‘animal_logic’ module from the backend to create an egg. The rarity and the cost of the egg will then be
returned as a JSON object.

Buy Eggs: POST /api/buy_egg/<string:username>

This endpoint is used to buy an egg. The user ID should be provided in the URL parameter. The server will
then check if username is valid (in the database). The request body should also include the data of the
egg (including its rarity and cost). If the user has sufficient coins, the server will deduct the amount from
the user's account and return a JSON object containing the updated user info, else an error message will
be returned.

Buy Eggs: POST /api/buy_listing/<string:username>

This endpoint is used to buy a listing item from the marketplace, the item can either be an egg or an
animal. The user ID (of the buyer) should be provided in the URL parameter. The server will then check if
username is valid (in the database). The request body should also include the data of the listing
(including its rarity and cost). If the user has sufficient coins, the server will deduct the listing amount
from the user's account and added to the seller’s balance. The item will then be transferred from the
seller’s inventory to the user’s (buyer’s) inventory, and the listing will be marked as sold and updated in
the database. The server will then return a JSON object containing the updated user info.

Fetching Eggs: GET /api/user/<string:username>/eggs

This endpoint is used to fetch data of all eggs that a user owns. The user ID should be provided in the
URL parameter. If the user exists in the database, the data of all eggs that the user currently owns will
then be returned as a JSON object.

Fetching Eggs: GET /api/user/<string:username>/animals

This endpoint is used to fetch data of all animals that a user owns. The user ID should be provided in the
URL parameter. If the user exists in the database, the data of all animals that the user currently owns will
then be returned as a JSON object.

Hatch Egg: POST /hatch

This endpoint is used to hatch an egg. The user and egg data should be sent within the request body. If
both the user and the egg (under user’s ownership) exists in the database, the egg will be hatched by
calling the ‘animal_logic’ module. The instance of the egg in the database will then be deleted and the
new animal will be added to the database. The server will return a JSON object containing the new
animal that hatched from the egg.

Update Coins: GET /api/update_coins

This endpoint is used to update the yielded coins of all animals that exists in the database. The coins
yielded for every animal is calculated based on the amount of time they have existed multiplied by the
specific coin yield for that animal. The coins yielded by each animal will then be updated in the database.
The server will then return a success message.

Burn Animal: POST /api/burn_animal

This endpoint is used to burn an animal. The user id and animal id data should be sent within the request
body. If both the user and the animal (under user’s ownership) exists within the database, the animal will
then be deleted from the database and the amount of coins the animal yielded will be added to the
user’s coin balance and updated in the database. The server will then return a JSON object containing a
success message containing coins yielded from the burned animal and the new balance.

Breed Animals: POST /api/breed_animals

This endpoint is used to breed two different animals to create a new hybrid animal. The animal IDs
should be provided in the request body. If both animals exists in the database, the two animals will be
bred together using the Breeder class logic from the ‘animal_logic’ module, the new animal’s (child of
the two animals bred) name will be a name merged from the two parent animals. The new animal will be
added to the database, while the two parent animals will be deleted from the database. The server will
return a JSON object containing a success message and the data of the new animal.

Listing on Market: POST /api/market_listing

This endpoint is used to make a new listing on the market. The user id (the seller), the item id (item to be
listed), listing name, item type (egg or animal) and listing price should be sent with the request body. If
item exists in user’s inventory in the database, the item will be transferred to the escrow user’s
inventory and a new market listing will be created and the database will be updated. The server will
return a JSON object containing a success message.

Get Listings: GET /api/listings

This endpoint is used to get all market listings that exist in the database. The server will return a JSON
object containing all listings that exist in the database.

Retrieve User Listings: POST /api/user_listings

This endpoint is used to retrieve all market listings made by a specific user. The username of user should
be sent in the request body. The server then checks the database for the username and returns the JSON
object of all the listings made by the user.

Update Listing: POST /api/update_listing

This endpoint is used to update a specific market listing. The listing id, updated listing name and updated
price should be sent in the request body. The server then checks the database for the listing, if the listing
exists, the new listing price and the new listing name will be updated in the database. The server then
returns a success message.

Cancel Listing: POST /api/cancel_listing

This endpoint is used to update a specific market listing. The listing id, user id should be sent in the
request body. The server then checks the database if the listing exists and if the listing was made by the
user id. The egg or animal in the listing will then be removed and added back into the inventory of the
user, listing status is also updated as ‘cancelled’ in the database. The server then returns a success
message.

Get Animal: GET /api/animal

This endpoint is used to check the owner of the animal, given the animal id. The animal id should be sent
in the request body. The server then checks the database for the user id (of the owner) of the animal id.
If the animal exists in the database, the server will return a JSON object containing a success message
and the data of the animal including the user id (of the owner).

Update Nickname: POST /api/update_nickname

This endpoint is used to update the nickname of an Animal. The animal id and nickname should be sent
in the request body. The server then checks the database for the animal id and updates the animal’s
nickname, the server then returns a success message.

Content-Type: Specifies the format of the data being sent or received (application/json)

The API uses the following status codes:

200 OK: The request was successful.

201 Created: The resource was created successfully.

400 Bad Request: The request was malformed.

404 Not Found: The requested resource could not be found.
Frontend

Figure 8 : Frontend Pages and Components

The frontend application is implemented using the Svelte framework, which is a reactive web framework
for building user interfaces. The user interface is designed to be simple and easy to use. The user
interface has been designed using Tailwind CSS, a utility-first CSS framework that provides a set of pre-
defined CSS classes to style HTML elements. The use of Tailwind CSS has made it easy to design and style
the user interface with a consistent look and feel.

The frontend application consists of 7 pages (Landing, Login, Register, Home, Market, Inventory and
Animal), 1 component (Navigation Bar) and 2 popups (Google Login, Google Register)

The frontend application communicates with the backend server through REST API calls. When the user
interacts with the web application, it sends requests to the backend server using the fetch() function in
JavaScript. The backend server then processes the requests and sends back responses that the frontend
application can use to update the user interface.

The frontend application is structured into multiple components, which are reusable building blocks that
can be composed to create more complex user interfaces. The use of components has made it easy to
organize the code and maintain the application as it grows in complexity.
Database

The CyberQuarium platform uses MySQL as its database management system. In this section, we will
describe the structure of the database, including the resources and their relationships.

The platform has four main resources/models: User, Egg, Animal, and MarketListing.

Figure 9 : ER Diagram

User: The users resource contains information about the users of the platform. The attributes of this
resource include user ID, username, email, password, coin balance and session id.

Egg: The eggs resource contains information about the eggs that users can buy, sell, and hatch. The
attributes of this resource include egg ID, rarity, cost, and the user id who currently owns the egg.

Animal: The animals resource contains information about the animals that users can buy, sell or breed to
create new animals. The attributes of this resource include animal ID, animal nickname, image ID, Date
of Birth, rarity, species, name, coin yield, coins yielded, and the user id who currently owns the animal.

MarketListing: The market listing resource contains information about the market listing that is listed by
a User. The attributes of this resource include market listing ID, user ID of the User who made the listing,
username, item ID, listing name, item type, price, name, image, rarity, yield rate of Animal (if the listing is
an Animal), whether the market listing sold and the cancelled status of the market listing.

The relationships between these resources are as follows:

A User can have many Eggs, Animals and MarketListings

An Egg belongs to one user and can be owned by only one user at a time.

An Animal belongs to one user and can be owned by only one user at a time.

A MarketListing belongs to one user and can be owned by only one user at a time.

To ensure data consistency and prevent data duplication, we use foreign keys to link the resources
together. The user ID is used as a foreign key in the eggs, animals and market listing resources. The
respective primary keys for each resources are the ids of the respective resources.
Backend

The CyberQuarium platform uses Flask as its backend server. Flask is a micro web framework written in
Python that allows developers to build web applications easily and quickly. For CyberQuarium, Flask was
chosen for its simplicity, flexibility, and Pythonic syntax. It is a good fit for the size and scope of the
project, as it allows us to quickly develop and deploy the backend server. Flask also has a large
community and a wealth of plugins and extensions available, making it easy to add additional
functionality as needed.

Another reason for using Flask is its compatibility with MySQL, which was chosen as the database for this
project. Flask comes with several extensions that provide easy integration with MySQL, allowing us to
easily manage database connections and execute SQL queries from within the Flask application.

Language:

The backend of the CyberQuarium platform is written in Python using Flask as the web framework.
Python is a high-level programming language that is widely used for web development, data analysis,
machine learning, and other fields.

Libraries and Packages:

The backend of the CyberQuarium platform uses several libraries and packages, including:

Flask-SQLAlchemy: This Flask extension package is an Object-Relational Mapping (ORM) library that
provides a high-level interface for interacting with relational databases.

Flask-Migrate: Flask extension that provides a simple way to handle database migrations in Flask
applications using SQLAlchemy. It allows developers to manage database changes and schema updates
easily, and also provides support for creating and running database migration scripts.

flask_cors: Flask extension for handling Cross-Origin Resource Sharing (CORS) requests. It provides
decorators that can be used to enable CORS for specific routes or globally across the entire application.
CORS is a security feature implemented by web browsers that prevents web pages from making requests
to a different domain than the one that served the original page.

Pyodbc: Python library that provides a Python Database API (PEP-249) interface for connecting to
Microsoft SQL Server and other databases using the Open Database Connectivity (ODBC) interface. It
enables interactions with SQL databases in a platform-independent way.

Requests: Python library for making HTTP requests. It provides a simple and intuitive way to interact with
web services and APIs by sending HTTP requests and receiving responses. It supports various HTTP
methods (e.g., GET, POST, PUT, DELETE), authentication, and cookies.

Nltk: (Natural Language Toolkit) is a Python library for working with human language data. It provides
tools for processing text data, such as tokenization, stemming, part-of-speech tagging, and named entity
recognition. It also includes corpora and resources for various languages and tasks, such as sentiment
analysis and machine translation.

g2p_en: Python library for converting graphemes (letters) to phonemes (sounds) in English words. It uses
machine learning techniques to predict the pronunciation of English words based on their spelling.

autopep8: Python library for automatically formatting Python code according to the PEP 8 style guide. It
can be used as a command-line tool or as a library in Python applications to automatically reformat code
and improve its readability.

Code Structure:

The CyberQuarium platform is structured into two portions, the frontend, and the backend.

The code is structured in multiple files and directories. The main files and directories are:

backend/flask_mssql_app/: This directory contains backend of CyberQuarium.

run.py: This file contains the main Flask server application.

routes.py: This file contains the REST API that the flask server of CyberQuarium serves.

models.py: This file contains the functions for connection to the SQL database server through
SQLAlchemy.

name_merger.py: This file contains the logic for merging names of two animals (after breeding)

classes.py: This file contains the backend logic for the implementation of Egg, Animals and Breeder
classes.

config.py: This file contains the API key to generate images for hybrid animals.

models.py: This file contains the database classes of the four resources: Egg, Animal, User and
MarketListing.

src/: This directory contains frontend of CyberQuarium.

src/components: This directory contains the svelte components message popup and navigation bar.

src/routes: This directory contains the svelte pages of animal, home, inventory, landing, listings, login,
market, and register.
Worklog

Week Jovian Lim Jie Chung Ong
1 Formed group^
2 Had meeting, decided to build a platform related to breeding virtual animals^
3 Researched suitable CSS framework to use, designed
the layout of the platform

Researched server and single page application
frontend framework to utilize for platform
4 Planned the Frontend and UI/UX of the platform^ Researched on database schema and frameworks^
5 Had meeting, finalized on CyberQuarium platform idea^
6 Started working on backend logic for eggs, animals,^
and breeding

Started working on report

7 Started working^ on Database^ Started working on server^
8 Setup the basic structure for the platform with
docker, worked on frontend UI

Researched and worked on authentication
methods, OAuth 2.
9 Finishing up on Application, preparation of Presentation^
10 Finishing up on codebase^ Finishing up on report^

