# Web Server for IoT Final Project


   
## Development 
This web server provides 2 endpoints for uploading weight data and usage history.

Example Endpoint for weight: ```/weight?timestamp=2022-04-09,12:12:12&catName=Haybe&value=20&userID=testUser```

Example Endpoint for usage: ```/usage?timestamp=1995-11-02,11:11:11&catName=Haybe&usageType=poop&userID=yunyuzhang11```

<br>

### Note
- URL and parameters are case sentisive. Please use lowercase for "poop" and "pee".<br>
- Timestamp's format is ```YYYY-mm-DD,HH:MM:SS```
- Check the ```testData.json``` for data examples. Feel free to test the endpoints with your own userID.


## Deployment
Depoly to google
by running ```gcloud run deploy```



## Useful Document
https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service


