This code will download records from the IRWIN database as a csv file.

Required: Create a file called creds.json. This data will be read and used to connect to the IRWIN hosted feature layer on ArcGIS Geoplatform. 
Copy the text below into the file and insert your username and password. Paste this text into creds.json and save it in the irwin_data_download folder.
{"username": "yourusername", "password": "yourpassword"}

There are 4 tables to download data from the IRWIN Database:
Incident: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/0
Incident Relationship: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/1
Incident Resource Summary: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/2
Incident History: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incident_History/FeatureServer/0

Modify the url on line 13 of main.py to point the code to a different table.
An example of the url:
https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/0/query?resultOffset={}

The SQL query used to specify which records to download is on line 17 of main.py. Modify this query to change which records will be downloaded. For example, CreatedBySystem = 'iroc', ModifiedOnDateTime > 1599605065170

Once the code completes, the records will be saved to a csv file in the same location as the code. To modify this file name or location, change line 57 of main.py.
