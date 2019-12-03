# src: https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777

# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3
RUN apt update
# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app
# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP
# Expose the port uWSGI will listen on
EXPOSE 5000
# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .
# Install Python dependencies
RUN pip install -r requirements.txt
# We copy the rest of the codebase into the image
COPY . .
# Finally, we run uWSGI with the ini file we
# created earlier
CMD [ "uwsgi", "--ini", "app.ini" ]


# ---------------
# Build for GKE & Register in Docker REgistry
# --
# gcloud builds --project elewa-portal-production submit --tag gcr.io/elewa-portal-production/assessment-reader:v1 .

# -- Inside GKE
# kubectl apply -f app.yaml
# kubectl expose deployment elewa-assessment-reader --type=LoadBalancer --port 80 --target-port 8080
# kubectl get services -l name=elewa-assessment-reader