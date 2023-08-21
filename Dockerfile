# FROM python:3.11.4
FROM selenium/standalone-firefox:latest


MAINTAINER Sohaib "sohaibayub9@gmail.com"

# Copy requirements.txt
COPY requirements.txt requirements.txt

# copy all folders and files
COPY facebook_page_scraper ./facebook_page_scraper
COPY .wdm ./.wdm
COPY BucketConnector.py BucketConnector.py
COPY ProxiesGrabber.py ProxiesGrabber.py
COPY .env .env

# Copy function code
COPY app.py app.py

# Use Root
USER root

# Download & Install PIP
# RUN apt-get install -y \
#     software-properties-common

# RUN add-apt-repository universe

RUN apt-get update && apt-get install -y \
    python3-pip

# Install the specified packages
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
