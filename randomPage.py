# Query the database and save current list of pages

from google.cloud import bigquery
import os
import pandas
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Alec/Python/bigQueryCreds.json"

client = bigquery.Client()

publicQuery = client.query("""
    SELECT
      Path 
    FROM `pagesreport.pagesreport_view`
    WHERE
  REGEXP_CONTAINS(Language, "en-GB|en-WLS")
  AND REGEXP_CONTAINS(Template, "Standard|Advice page|Beta content page|AdviserNet page|Legacy AdviserNet page|Leaflet|Sample letter|Form|Document|Universal Credit|Energy comparison|Court Nav")
  AND REGEXP_CONTAINS(Path, "^/(benefits|consumer|debt-and-money|family|health|housing|immigration|law-and-courts|work)/")
  AND StopPublish IS NULL
  AND NOT IsTranslation""")

adviserQuery = client.query("""
    SELECT
      Path 
    FROM `pagesreport.pagesreport_view`
    WHERE
  REGEXP_CONTAINS(Language, "en-GB|en-WLS")
  AND REGEXP_CONTAINS(Template, "Standard|Advice page|Beta content page|AdviserNet page|Legacy AdviserNet page|Leaflet|Sample letter|Form|Document|Universal Credit|Energy comparison|Court Nav")
  AND REGEXP_CONTAINS(Path, "^/(advisernet/benefits|advisernet/consumer|advisernet/debt-and-money|advisernet/family|advisernet/health|advisernet/housing|advisernet/immigration|advisernet/law-and-courts|advisernet/work)/")
  AND StopPublish IS NULL
  AND NOT IsTranslation""")

publicResults = publicQuery.result()  # Waits for job to complete.
#adviserResults = adviserQuery.result()

results = publicResults.to_dataframe()

print(results)