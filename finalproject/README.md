# PermaBulk
#### Video Demo:  https://www.youtube.com/watch?v=JQ_MRRj0N7c
#### Description: My final project for CS50 is "PermaBulk" a python-flask web app for fitness program tracking.  

### After creating an account PermaBulk lets you choose a fitness program. The chosen program with it's given exercises, sets and reps gets displayed on the "My Program" page. On this page you can input the sets and reps you do during a workout and then press the button for an in page timer. After completing a workout by pressing the "Finish Workout" button your performance gets stored in the database to build upon the next time you have this specific day in your workout. By finishing a workout the database gets updated so now your next workout is ready for you on the "My Workout" page. Additionally there is a one rep max calculator, a recipe page and a statistics page to help you on your fitness journey. 


## Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* Jinja
* SQLite

## Pages
The PermaBulk web app consists of the following pages.
* Home
* Programs
* Recipes
* Statistics
* 1 Rep Max
* My program
* Log in / Log Out
* Register

## Usage
1. Home page: this is the landing page of PermaBulk, upon entering the home page a random quote is shown. From the home page you can navigate to all other pages.

2. Programs page: the programs page displays all on PermaBulk available as cards with a short description. On this page you can enroll in a new program. It has a live search bar to search for programs.

3. Recipes page: the recipe page shows a number of high protein/bulking recipes for the interested, to accompany your new fitness journey with better eating habits. It has a live search bar to search for recipes.

4. Statistics page: upon finishing a workout all your results are stored, PermaBulk fetches your best main lift and calculates your "one rep max" using the ekley formula together with the date of your workout and displays it with the other main lifts on this page to track progress over time.

5. 1 Rep Max page: on this page you can calculate your one rep max manually. If you update the one rep max of a specific lift the value gets used as a starting point for your fitness program.

6. My program page: the program you're following gets dynamically shown here. PermaBulk fetches your program progress and shows the corresponding Day, exercises, sets and reps. After completing an exercise you're able to press a button for a 2 minute timer. After completing all exercises you can press "Finish Workout" your program gets rolled over to the next day and progress is stored.

7. Log in / Log out pages: allows users to log in or log out of the PermaBulk app.

8. Register page: allows new users to create an account and acces the programs to start lifting.

# Files

## Static

### **styles.css**
##### This file contains all local css

### **favicon.ico**
##### This is a miniature version of the PermaBulk logo to show in browser tab. 

### **logo.png**
##### A stockphoto of a blue barbell used as logo for PermaBulk.

### **service-bell**
##### Mp3 file that contains the ringing sound for the timer on the workout page.

### **chart.js**
##### JavaScript file that contains all the JavaScript for the chart on the statistics page. This is a seperate file because it gives an error on pages with no canvas.

### **main.js**
##### The bulk of the JavaScript used on PermaBulk. Usage consists of the timer, a live search bar used on multiple pages, one rep max calculation and the fading of flash messages.

## Templates

### **current_program.html**
##### Bread and butter of PermaBulk. This page dynamically shows you exercises for the specific day in your program.

### **index.html**
##### The landing page of PermaBulk.

### **layout.html**
##### My project uses jinja. This layout is the blueprint for every page in this project. It containts a responsive navbar that collapses and provides all flash messages. It also contains the header which consists of the links and script such as bootstrap, css, jquery, popper.js, chart.js and javascript.

### **login.html**
##### Log in page, my project uses Flask and flask_session for authorization.

### **onerepmax.html**
##### This page lets you update your one rep max manually using the ekley formula in the backend. At the bottom you have a live calculator to calculate your one rep max for a certain exercise.

### **programs.html**
##### On this page all available programs are shown in card form. The page also has a live search bar.

### **recipes.html**
##### On this page all available recipes are shown in card form. The page also has a live search bar.

### **statistics.html**
##### Shows your progress over time by showing you your one rep max on a certain date.

## **app.py**
##### This file contains the bulk of the python code for this project. It is responsible for all routing and authorization.

## **functions.py**
##### This file contains functions for some often repeated tasks, such as db_query, db_modify, db_fetch and get_stats.

## **permabulk.db**
##### SQLite database responsible for storing all progress, users, programs, recipes, etc.

## **README.md**
##### This file describes my project and it's contents.







## Acknowledgements
This project was developed as a final project for CS50.