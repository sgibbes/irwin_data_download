This code will download records from the IRWIN database as a csv file.

There are 4 tables to download data from the IRWIN Incidents Database:
Incident: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/0
Incident Relationship: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/1
Incident Resource Summary: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/2
Incident History: https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incident_History/FeatureServer/0

Modify the url on line 13 of main.py to point the code to a different table.

The SQL query used to specify which records to download is on line 17 of main.py. Modify this query to change which records will be downloaded. For example, CreatedBySystem = 'iroc' or ModifiedOnDateTime > 1599605065170

Once the code completes, the records will be saved to a csv file in the same location as the code. To modify this file name or location, change line 57 of main.py.
