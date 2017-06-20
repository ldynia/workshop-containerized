FROM alpine:3.6

MAINTAINER Lukasz Dynowski ludd@cbs.dtu.dk

# Copy app dir form host into image
COPY ./app /app
WORKDIR /app

# OS Update & Upgrade
RUN apk update && apk upgrade

# Install packages
RUN apk add \
  python \
  py-pip

# Install application wide packages
RUN pip install -r requirements.txt

# Execute script as a global program
RUN ln -s /app/main.py /usr/local/bin/fsa-analyzer
RUN chmod +x /usr/local/bin/fsa-analyzer

# Startup script
#CMD ["sh", "/app/scripts/startup.sh"]
