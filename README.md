# car-dealership

![car-dealership-index.html page](https://github.com/rayray39/car-dealership/blob/main/car-dealership%201.png)

## General Description
This is a simple website project built over a weekend that allows users to auction for cars (imagine eBay, but for cars only), similar to a car dealership. Users can **post a new auction listing**, **place bids** on other auction listings and **leave reviews**. Other features include a **Watchlist feature** - where users can add the auction listings, that they would like to keep an eye on, to a page for easier navigation. It also includes a **Category feature** - where users can quickly navigate to the type of car they are interested in looking at (such as SUV, Sedan, Supercar etc.).

## Instructions For Use
Make sure you have `python` and `django` installed in a virtual environment. Download the folders in the **master branch** to a local folder with the virtual environment. The following steps should be run in the command prompt (CMD). Navigate to the folder containing this project. Firstly, make sure to run `python manage.py makemigrations cars` to generate the set of "instructions" for Django to know what has been updated and changed within the model. Secondly, run `python manage.py migrate` to actually allow Django to implement the set of "instructions". Lastly, run `python manage.py runserver` to run the app in a local server. 

## File Descriptions
* models.py - contains the Django models (the tables of the database). 
* views.py - the functions that render the different HTML pages and the logic to interact with the data inside the database. 
* templates - the various HTML pages. 
* static - the CSS files used for styling. 
* urls.py (inside app) - the various url paths that will call the associated function in views.py to render a HTML page. 

## Lessons Learnt
* developing an interactive website using a web framework like Django, Python, HTNL and CSS.
* using Django models that allow easy interaction with data stored inside the database, removing the need to write SQL commands.
* implementing client-side and server-side validation checks when filling up forms.
* using flex layout in CSS.

## Disclaimer
This project's inspiration was taken from **Harvard's CS50 Web Programming with Python and JavaScript** course, where I am, at the time of writing, enrolled in.  
