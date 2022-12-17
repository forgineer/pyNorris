"""
   Program Name:  PyNorris.py
   Author:        Blake Phillips
   Description:   Chuck Norris Joke Generator

   Utilizes the chucknorris.io API for retrieving random Chuck Norris "facts" jokes or jokes based on a set of categories given by the API

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
   "value":"Whitney Houston was recently found dead in a Hotel room with drugs all around her body. She overdosed once she found out Chuck Norris was actually her father."
   }'
"""
from tkinter import *
from PIL import Image, ImageTk   # pip install pillow
#import Image, ImageTk
import http.client
import json
import sqlite3
import time


# Define Global Variables
baseURL = "api.chucknorris.io"
pathRandom = "/jokes/random"
pathCategories = "/jokes/categories"

# Set base HTTP connection string
apiConnect = http.client.HTTPSConnection(baseURL)


# Define Program Functions
def getCategories():
   apiConnect.request("GET", pathCategories)
   respCategories = apiConnect.getresponse()

   if(respCategories.status == 200):
      jsonCategories = respCategories.read()
      catList = json.loads(jsonCategories)
      catList.insert(0, 'random')   # Include 'random' as the first option in the list

      #print(categories)
      #for category in categories: # Traversal of List sequence
      #   print(category)
      return catList
   else: # If no connection, make 'random' the only choice in the list
      catList = ['random']
      return catList

def getJoke():
   if(optionVar.get() != 'random'):
      getCategoryStr = pathRandom + "?category=" + optionVar.get()
      apiConnect.request("GET", getCategoryStr)
      respJoke = apiConnect.getresponse()
   else:
      apiConnect.request("GET", pathRandom)
      respJoke = apiConnect.getresponse()

   #print(optionVar.get())
   #apiConnect.request("GET", pathRandom)
   #respJoke = apiConnect.getresponse()
   
   if(respJoke.status == 200):
      #print(respJoke)
      jokeJSON = respJoke.read()
      #print(jokeJSON)
      jokeList = json.loads(jokeJSON)
      #print(jokeList["value"])
      jokeText.set(jokeList["value"])

      # Store the joke in local DB (PyNorris.db)
      jokeId = jokeList["id"]
      jokeCreateDtTm = jokeList["created_at"]
      jokeValue = jokeList["value"]

      storeFlg = storeJoke(jokeId, jokeCreateDtTm, jokeValue)
   else:
      jokeText.set("For some reason I wasn't able to get a new joke. Try again in a minute")

def storeJoke(pId, pDate, pValue):
   dbConnect = sqlite3.connect('PyNorris.db')
   dbCursor = dbConnect.cursor()

   sqlStr = "SELECT ID FROM JOKES WHERE ID = '" + pId + "'"
   dbCursor.execute(sqlStr)
   row_count = dbCursor.rowcount

   if(row_count <= 0):
      localtime = time.localtime(time.time())

      year = str(localtime[0])
      month = str(localtime[1])
      day = str(localtime[2])
      hour = str(localtime[3])
      minute = str(localtime[4])
      second = str(localtime[5])

      stored_dt_tm = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
      #print(stored_dt_tm)

      sqlStr = "INSERT INTO JOKES (ID, CREATED_AT, VALUE, STORED_DT_TM) VALUES(?, ?, ?, ?)"
      dbCursor.execute(sqlStr, (pId, pDate, pValue, stored_dt_tm))
      dbConnect.commit()
      dbConnect.close()
   
   return 1 # true


# *** Main Program Start ***

# Setup root window
pyNorrisWindow = Tk()
pyNorrisWindow.title("PyNorris")
pyNorrisWindow.geometry("784x442")
pyNorrisWindow.resizable(width=False, height=False)

# Set label for background image of Chuck Norris
img = Image.open("chuck_norris_bubble.jpg")
norrisImg = ImageTk.PhotoImage(img)
bgLabel = Label(pyNorrisWindow, image=norrisImg)
bgLabel.place(x=0, y=0)

# Set drop-down list of category options for Chuck Norris jokes
optionVar = StringVar()
optionVar.set('random') # Set random by default
categories = getCategories()
categoryOptions = OptionMenu(pyNorrisWindow, optionVar, *categories)
categoryOptions.place(x=5, y=405)

# Set button for getting a new Chuck Norris joke and displaying it
jokeButton = Button(pyNorrisWindow, text="Get Joke!", command=getJoke)
jokeButton.place(x=105, y=408.5)

# Set Joke text label over image word bubble
jokeText = StringVar()
jokeLabel = Label(pyNorrisWindow, textvariable=jokeText, bg="yellow", wraplength=180)
jokeText.set("Click the 'Get Joke!' button for a Chuck Norris fact!")
jokeLabel.place(x=580, y=180)

# Start up the PyNorris GUI program!
pyNorrisWindow.mainloop()

# *** Main Program End ***