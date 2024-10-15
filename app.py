import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
import psycopg2
from psycopg2 import sql
import urllib.parse as urlparse

from config import Config


VIDEO_NUM = 6

config = Config.get_config()

#heroku
DATABASE_URL = config['DATABASE_URL']
SURVEY_BASE_URL = config['SURVEY_BASE_URL']
#local



@app.route("/")
def helloworld():
    return "Hello World!"

@app.route('/display', methods=['GET'])
def display_videos():
    rows = retrieve_videos()
    #display the rows in an html table
    html = "<table>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table>"
    return html

def retrieve_videos():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()


        #load the query text from retrieve_videos.sql
        query_text = open("retrieve_videos.sql", "r").read()
        cur.execute(query_text)
        #modify this to user the increment counter and the genre so we get one video from each genre

        # Fetch and print the result of the query
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    
    return(rows)


@app.route('/survey_redirect', methods=['GET'])
def survey_redirect():
    query_string = request.query_string.decode()
    print(query_string)
    
    #need to add update logic to increment counter for each video served
    #
    rows = retrieve_videos()
    
    query_params = {}
    for row_i, row in enumerate(rows):
        query_params[f'v{row_i}u'] = row[1]
        query_params[f'v{row_i}id'] = row[2]

    query_string += "&" + urlparse.urlencode(query_params)
    print(query_string)

    #redirect back to the survey 
    return redirect(SURVEY_BASE_URL + "?" + query_string)

# virtualenv --python="/usr/local/bin/python3" 
# run the app
if __name__ == '__main__':
    app.run(debug=True)


