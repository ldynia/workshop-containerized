FROM alpine:3.6

MAINTAINER Lukasz Dynowski ludd@cbs.dtu.dk

COPY ./app /app
WORKDIR /app

# Update packages
RUN apk update
RUN apk upgrade

# Install OS wide packages
RUN apk add bash
RUN apk add python
RUN apk add py-pip
RUN apk add vim

# Install application wide packages
RUN pip install -r requirements.txt

# Execute script as a global program
RUN ln -s /app/main.py /usr/local/bin/fsa-analyzer
RUN chmod +x /usr/local/bin/fsa-analyzer

# Force containter to stay up fornt
#CMD ["bash", "scripts/startup.sh"]
