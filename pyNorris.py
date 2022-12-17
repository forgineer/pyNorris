"""
   Program Name:  pyNorris.py
   Author:        Blake Phillips
   Description:   Chuck Norris Joke Teller

   Utilizes the chucknorris.io API for retrieving Chuck Norris "facts" or jokes at random or based on a given
   category provided by the API.

   https://api.chucknorris.io/jokes/random
   https://api.chucknorris.io/jokes/categories
   https://api.chucknorris.io/jokes/random?category={category}

   JSON response example:
   '{
   "categories":[],
   "created_at":"2020-01-05 13:42:21.179347",
   "icon_url":"https://assets.chucknorris.host/img/avatar/chuck-norris.png",
   "id":"hNut57c3Q7qPmIGi57LKog",
   "updated_at":"2020-01-05 13:42:21.179347",
   "url":"https://api.chucknorris.io/jokes/hNut57c3Q7qPmIGi57LKog",
   "value":"Whitney Houston was recently found dead in a Hotel room with drugs all around her body. She overdosed once
   she found out Chuck Norris was actually her father."
   }'
"""
from tkinter import *
from PIL import Image, ImageTk  # pip install Pillow
import http.client
import json
import logging
import sqlite3
import time

# Set log level for debugging
# logging.basicConfig(level=logging.DEBUG)

# Define Base URL and Paths for chucknorris.io API
baseURL = "api.chucknorris.io"
pathRandom = "/jokes/random"
pathCategories = "/jokes/categories"

# Set base HTTP connection string
apiConnect = http.client.HTTPSConnection(baseURL)


def getCategories():
    logging.info("Retrieving joke categories...")

    apiConnect.request("GET", pathCategories)
    respCategories = apiConnect.getresponse()

    if respCategories.status == 200:
        jsonCategories = respCategories.read()
        catList = json.loads(jsonCategories)
        catList.insert(0, 'random')  # Include 'random' as the first option in the list

        logging.debug(f'List of Categories: {catList}')

        return catList
    else:  # If no connection, make 'random' the only choice in the list
        logging.info("Unable to retrieve categories, random only...")
        catList = ['random']
        return catList


def getJoke():
    logging.info(f'Getting next {optionVar.get()} joke...')

    if optionVar.get() != 'random':
        getCategoryStr = pathRandom + "?category=" + optionVar.get()
        apiConnect.request("GET", getCategoryStr)
        respJoke = apiConnect.getresponse()
    else:
        apiConnect.request("GET", pathRandom)
        respJoke = apiConnect.getresponse()

    if respJoke.status == 200:
        jokeJSON = respJoke.read()
        logging.debug(f'Response: {jokeJSON}')

        jokeDict = json.loads(jokeJSON)  # Load JSON as dictionary
        logging.debug(f'JSON list: {jokeDict}')

        jokeText.set(jokeDict["value"])  # Set bubble text

        # Store the joke in local DB (PyNorris.db)
        jokeId = jokeDict["id"]
        jokeCreateDtTm = jokeDict["created_at"]
        jokeValue = jokeDict["value"]

        if not jokeDict["categories"]:
            jokeCategory = "random"
        else:
            jokeCategory = jokeDict["categories"][0]

        logging.debug(f'id: {jokeId}')
        logging.debug(f'created_at: {jokeCreateDtTm}')
        logging.debug(f'value: {jokeValue}')
        logging.debug(f'categories: {jokeCategory}')

        storeJoke(jokeId, jokeCreateDtTm, jokeValue, jokeCategory)
    else:
        jokeText.set("For some reason I wasn't able to get a new joke. Try again later.")


def storeJoke(pId, pDate, pValue, pCategory):
    dbConnect = sqlite3.connect('pyNorris.db')  # Creates DB if not exists
    dbCursor = dbConnect.cursor()
    jokeExists = False

    try:
        sqlStr = "SELECT id FROM jokes WHERE id = '" + pId + "'"
        dbCursor.execute(sqlStr)

        if dbCursor.rowcount > 0:
            jokeExists = True
    except:
        logging.exception("Failed to check if joke is already stored. The table probably did not exist. Creating...")

        # Create JOKES table if not exist
        sqlStr = """
            CREATE TABLE jokes(
                id TEXT,
                created_at TEXT,
                value TEXT,
                category TEXT,
                stored_dt_tm TEXT
            )
        """
        dbCursor.execute(sqlStr)
        dbConnect.commit()

    if not jokeExists:
        localtime = time.localtime(time.time())

        year = str(localtime[0])
        month = str(localtime[1])
        day = str(localtime[2])
        hour = str(localtime[3])
        minute = str(localtime[4])
        second = str(localtime[5]).rjust(2, '0')

        stored_dt_tm = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
        logging.debug(f'Joke will be stored at {stored_dt_tm}')

        sqlStr = "INSERT INTO jokes (id, created_at, value, category, stored_dt_tm) VALUES(?, ?, ?, ?, ?)"
        dbCursor.execute(sqlStr, (pId, pDate, pValue, pCategory, stored_dt_tm))
        dbConnect.commit()
        dbConnect.close()


# Main
# Setup root window
pyNorrisWindow = Tk()
pyNorrisWindow.title("pyNorris")
pyNorrisWindow.geometry("784x442")  # Size of the background image
pyNorrisWindow.resizable(width=False, height=False)

# Set label for background image of Chuck Norris
img = Image.open("images/chuck_norris_bubble.jpg")
norrisImg = ImageTk.PhotoImage(img)
bgLabel = Label(pyNorrisWindow, image=norrisImg)
bgLabel.place(x=0, y=0)

# Set drop-down list of category options for Chuck Norris jokes
optionVar = StringVar()
optionVar.set('random')  # Set random by default
categories = getCategories()
categoryOptions = OptionMenu(pyNorrisWindow, optionVar, *categories)
categoryOptions.place(x=5, y=400)

# Set button for getting a new Chuck Norris joke and displaying it
jokeButton = Button(pyNorrisWindow, text="Get Joke!", command=getJoke)
jokeButton.place(x=105, y=400)

# Set Joke text label over image word bubble
jokeText = StringVar()
jokeLabel = Label(pyNorrisWindow, textvariable=jokeText, bg="yellow", wraplength=180)
jokeText.set("Click the 'Get Joke!' button for a Chuck Norris fact!")
jokeLabel.place(x=580, y=221)

# Start up the PyNorris GUI program!
pyNorrisWindow.mainloop()
