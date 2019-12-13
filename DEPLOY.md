# DEPLOYMENT OF THE ELEWA ASSESSMENT OCR

Created on 11/12/2019
Author: Zeddy Jeremani – Software Eng.


## Prefix

The Elewa Assessment OCR is a python application that contains the scanning algorithm that is consumed by the Elewa App Batch Marking system. This application is hosted on GCP (Google Cloud Platform) servers and runs inside of a docker container, with the help of a flask server for HTTP requests and nginx.


## Prerequisites 

Before deploying, let’s make sure that you’ve got everything set. Listed below are some of the prerequisites that you are going to need: 

*	Code to deploy – You’ll need all the new code that you are going to push to GCP servers. Obviously.  

*	Access to Elewa GCP servers – You’ll need access to Elewa GCP to do any kind of deployment to the servers. To confirm if you have access to Elewa GCP servers, login to Google Cloud Platform with your work email, click on console and confirm if you see some of the Elewa Projects. If you don’t have access to Elewa GCP servers, contact your supervisor. 
   
*	The Google Cloud SDK – Make sure that you’ve got the Google Cloud SDK installed on your machine. You’ll need this to deploy your changes through your terminal or command. To check if you have the Google Cloud SDK installed, open up terminal or command and enter this command: `gcloud --version`.

To download, install and initialize the Google Cloud SDK refer here: [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-versioned-archives)


## Process Deployment

To successfully deploy a version of the Elewa Assessment OCR Application, follow these steps: 

1.	Deploy your new code onto Elewa GCP servers - Open up your terminal or Command and run this command: 

`sudo gcloud compute scp --recurse [name of vm instance]:[path to copy to inside vm instance]`

Example:

`sudo gcloud compute scp --recurse wns-elewa-app:/home/JRossel/build`

To deploy a single file, run this command:
`sudo gcloud compute scp [path to the single file being pushed]  [name of vm instance]:[path to copy to inside vm instance]`

Example (To deploy a single file – init-letsencrypt.sh):

`sudo gcloud compute scp ./init-letsencrypt.sh  wns-elewa-app:/home/JRosseel/build/elewa-assessment-ocr`

2.	SSH into the appropriate VM instance on GCP to docker-compose up. 
    I.	Log into GCP using your work email and click on console. 
    II.	Click on the menu icon on the top left. 
    III.	Navigate to Compute Engine > VM instances
    IV.	SSH into the appropriate VM instance. 
    V.	Inside the online console, CD into the directory where you pushed your code to.
    `cd /home/JRossel/build/[name of the project]`

    In the above example that would be: 
    `cd /home/JRossel/build/elewa-assessments-ocr`

    VI.	Run the command: `docker-compose up --build`

If everything went well, your new changes should have taken effect. 


## Problems you may run into

In the process of deployment, you may run into some issues. We’ve tried to document some of these issues and how we solved them. (This section is updated regularly). 

1.	A docker-compose up --build error – You may experience problems running docker-compose up. This may be caused by various reasons. However, be sure that you are running this command from the root of your project folder. Make sure that you have a docker-compose.yml file in your root. To check this simply enter the command ls to list all files in the current directory. If you experience a different error, contact your supervisor for help. 

2.	A gcloud scp error – If you experience issues pushing the project code onto gcp, this may be as a result of a couple of things: 

i.	You’re Google Cloud SDK may not be configured correctly. 
ii.	You do not have the right permissions to push to Elewa GCP servers. 
iii.	You are probably trying to push to the wrong project. 


## Extra Notes

No extra notes – (This section is updated regularly)