import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
import psycopg2
from psycopg2 import sql
import urllib.parse as urlparse


VIDEO_NUM = 10

#heroku
DATABASE_URL = os.getenv('DATABASE_URL')
SURVEY_BASE_URL = os.getenv('SURVEY_BASE_URL')
#local

conn = psycopg2.connect(DATABASE_URL)

@app.route("/")
def helloworld():
    return "Hello World!"

@app.route('/survey_redirect', methods=['GET'])
def survey_redirect():
    query_string = request.query_string.decode()
    print(query_string)
    
    try:
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Sample query to verify connection (fetch PostgreSQL version)
        cur.execute(f"SELECT video_creator_username, video_site_id FROM videos LIMIT {VIDEO_NUM};")
        #modify this to user the increment counter and the genre so we get one video from each genre

        # Fetch and print the result of the query
        rows = cur.fetchall()
    finally:
        cur.close()

    #need to add update logic to increment counter for each video served
    #
    
    query_params = {}
    for row_i, row in enumerate(rows):
        query_params[f'v{row_i}u'] = row[0]
        query_params[f'v{row_i}id'] = row[1]

    query_string += "&" + urlparse.urlencode(query_params)
    print(query_string)

    #redirect back to the survey 
    return redirect(SURVEY_BASE_URL + "?" + query_string)

# virtualenv --python="/usr/local/bin/python3" 
# run the app
if __name__ == '__main__':
    app.run(debug=True)