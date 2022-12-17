# pyNorris
This is an older project that I completed in 2019 while a co-worker and I were learning Python together for the first time, and after completing a set of online tutorials we decided to test ourselves with a final project before moving on to another language. For this final project, I decided to [re-use this idea](https://github.com/forgineer/ChuckNorrisIO) of creating a front-end application that would retrieve Chuck Norris jokes from the [Chuck Norris IO API](https://api.chucknorris.io/). The set of online tutorials we followed can be found at [TutorialsPoint.com](https://www.tutorialspoint.com/python3/index.htm).

## How it Works...
Running the `pyNorris.py` module application will present the user with a very simple interface that includes a background picture of Chuck Norris with a speech bubble. The speech bubble will contain some default text encouraging the user to get a new joke. In the bottom left-hand corner of the application are a drop-down and a button.

<p align="center">
  <img src="/images/pyNorris_demo1.png">
</p>

The drop-down contains a list of available joke categories that the user can select for a specific type of joke they would like to get from the [Chuck Norris IO API](https://api.chucknorris.io/). The "Get Joke!" button will retrieve a new joke by calling the API and displaying it in the speech bubble.

<p align="center">
  <img src="/images/pyNorris_demo2.png">
</p>

After retrieving the joke from the API, before displaying the joke in the speech bubble, the joke will be stored in a local SQLite database including some additional metadata from the API and a timestamp when the joke was stored.

<p align="center">
  <img src="/images/pyNorris_demo3.png">
</p>