# Film Review Website - Flask

## Table of Contents
* [Technologies](#technologies)
* [Introduction](#introducion)
* [Website Components](#Website-components)
* [Welcome Page](#welcome-page)
* [Film Details](#Film-details)
* [Registration](#registration)
* [Note](#note)
* [Comments](#comments)
* [Requirements](#requirements)
* [To run the Website locally](#to-run-the-website-locally)
* [Acknowledgments](#acknowledgments)

## Technologies
* [Flask 2.2.2](https://flask.palletsprojects.com/)
* [Bootstrap](https://getbootstrap.com/)

## Introduction
The website I have developed presents the user with the Films, allowing them to be searched and sorted according to selected criteria. The website allows logged-in users to write their thoughts on a given Film, which are visible only to the author of a note, as well as to join a public discussion on a selected Film. 

## Website Components

### Welcome Page
![image](https://github.com/Gorwik/Film-Review-Website---Flask/assets/101866409/28166120-ff2c-499f-9eea-53ac21e5a997)

The welcome page displays the videos sorted by current popularity. The browser allows searching Films by title, year of production, genre and minimum acceptable rating.

### Film Details
![image](https://github.com/Gorwik/Film-Review-Website---Flask/assets/101866409/0a48e8e0-c803-4b45-b23b-996d2f21f909)

By clicking on the thumbnail of the Film's poster, the page is displayed which shows details of the Film.

### Registration
![image](https://github.com/Gorwik/Film-Review-Website---Flask/assets/101866409/06f99ba7-dbaf-4bd4-9f98-4cac0fa8613d)

The site allows for the registration of new users. Passwords are stored hashed in the database.

### Note
![image](https://github.com/Gorwik/Film-Review-Website---Flask/assets/101866409/7335e10f-6e99-4c6e-8bb0-c55d8c099ff3)

Any logged-in user, can leave a note with their thoughts on the Film. The note is private, it is only visible to the author of the note. The note can be changed or completely deleted.

### Comments
![image](https://github.com/Gorwik/Film-Review-Website---Flask/assets/101866409/81cd4152-01fd-4058-b925-d43687bc9ff8)

Any logged-in user can leave a public comment after the video. Any comment can be deleted but not modified. It is possible to add replies to previously posted comments. These are then visible in the form of a comment tree.  

## Requirements:
- Python version 3.10
- Account and API_KEY on [TMDB](https://developer.themoviedb.org/docs/getting-started)
  
### To run the Website locally:
1. In root folder create .venv environment.  
``
python -m venv Film-review-env
``

1. Activate it.  
On Windows:  
``
Film-review-env\Scripts\activate
``  
On Unix or MacOS:  
``
source Film-review-env/bin/activate
``  

1. Install dependencies included in [requirements.txt](https://github.com/Gorwik/Film-Review-Website---Flask/blob/master/requirements.txt).   
``
pip install -r requirements.txt
``  

1. Set up API keys.  
On Windows:  
``
setx TMDB_API_KEY "your-TMDB-key-here"
``  
On Unix or MacOS:  
``
exportTMDB_API_KEY='your-TMDB-key-here'
``
## Acknowledgments
- [Flask foundations](https://www.youtube.com/playlist?list=PLzMcBGfZo4-nK0Pyubp7yIG0RdXp6zklu)
