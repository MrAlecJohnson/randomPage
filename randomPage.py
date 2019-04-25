# Query the database and save current list of pages

from google.cloud import bigquery
import os
import flask
import json

# Get the data from BigQuery
# Set credentials for local use - not needed for live as it's stored on Heroku
#os.environ["GOOGLE_JSON"] = "/Users/alec/Python/randomPage/bigQueryCreds.json"

client = bigquery.Client()

publicQuery = client.query("""
    SELECT
      Path, MainTitle
    FROM `pagesreport.pagesreport_view`
    WHERE
  REGEXP_CONTAINS(Language, "en-GB|en-WLS")
  AND REGEXP_CONTAINS(Template, "Standard|Advice page|Beta content page|AdviserNet page|Legacy AdviserNet page|Leaflet|Sample letter|Form|Document|Universal Credit|Energy comparison|Court Nav")
  AND REGEXP_CONTAINS(Path, "^/(benefits|consumer|debt-and-money|family|health|housing|immigration|law-and-courts|work)/")
  AND StopPublish IS NULL
  AND NOT IsTranslation
  """)

adviserQuery = client.query("""
    SELECT
      Path, MainTitle
    FROM `pagesreport.pagesreport_view`
    WHERE
  REGEXP_CONTAINS(Language, "en-GB|en-WLS")
  AND REGEXP_CONTAINS(Template, "Standard|Advice page|Beta content page|AdviserNet page|Legacy AdviserNet page|Leaflet|Sample letter|Form|Document|Universal Credit|Energy comparison|Court Nav")
  AND REGEXP_CONTAINS(Path, "^/(advisernet/benefits|advisernet/consumer|advisernet/debt-and-money|advisernet/family|advisernet/health|advisernet/housing|advisernet/immigration|advisernet/law-and-courts|advisernet/work)/")
  AND StopPublish IS NULL
  AND NOT IsTranslation
  """)

publicResults = publicQuery.result()  # Waits for job to complete.
adviserResults = adviserQuery.result()

public = publicResults.to_dataframe()
adviser = adviserResults.to_dataframe()

# %%

# Function to pick the random pages
def picker(public, adviser):
    publicPage = public.sample(1)
    adviserPage = adviser.sample(1)
    return (publicPage.iloc[0]['MainTitle'],
            publicPage.iloc[0]['Path'],
            adviserPage.iloc[0]['MainTitle'],
            adviserPage.iloc[0]['Path'])

prefix = "https://www.citizensadvice.org.uk"

# %%

# Set up the flask app
app = flask.Flask(__name__)

@app.route('/random', methods = ["GET"])
def index():
    pages = picker(public, adviser)
    return flask.render_template('randomPage.html',
                                 publicPage = str(pages[0]),
                                 publicUrl = prefix + str(pages[1]),
                                 adviserPage = str(pages[2]),
                                 adviserUrl = prefix + str(pages[3])
                                 )

if __name__ == '__main__':
    app.run(debug = True, port = 5000)
