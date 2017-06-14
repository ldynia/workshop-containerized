# Containerized Workshop
This repository was create as a demo project to demonstrate usage of containerized technologies ([docker](https://docs.docker.com/) and [singularity](http://singularity.lbl.gov/)).

Objectives are to show scientists the beast practices using containerized technologies. You will learn how to package, distribute and share software using containerized technology.

# Docker
## Requirements
Below requirements have to be full field.
* [git](https://git-scm.com/downloads) - installed
* [docker](https://docs.docker.com/) - installed
* [dockerhub](https://hub.docker.com/) account
* [docker-compose](https://docs.docker.com/compose/install/#alternative-install-options) account
* [pytohn](https://www.python.org/downloads/) -installed
* [pip](https://pypi.python.org/pypi/pip) -installed
* sudo/root access yours machine

```
# Check if service is running
user@machine:~$ sudo service docker status
[sudo] password for user:
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2017-06-13 16:41:02 CEST; 21h ago


# Check if user belongs to docker group
user@machine:~$ groups
adm sudo staff users vboxusers docker
```


## Git
Execute below instructions.

```
# Go to home directory
user@machine:~$ cd ~

# Clone repository
user@machine:~$ git clone https://github.com/ldynia/containerized-workshop

# Go to repository dir
user@machine:~$ cd containerized-workshop

# Remove these files
user@machine:~/containerized-workshop$ rm -rf composer-app.yml Dockerfile app/scripts/

```
## Program Part I
Program provides statistical data on fsa file. Input of the program is *fsa* file. Output of the program is number of nucleotides and codons. **Note:** Program returns output after 5s -this is intended behavior.

```
# Go to app directory
user@machine:~/containerized-workshop$ cd app

# Run program and pritify its output
user@machine:~/containerized-workshop/app$ python main.py data/dna.fsa | python -m json.tool
{
    "nucleotides": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}

```

## Docker Image Part I
Lets start with docker image first. Docker **image** is nothing more than a executable package (exactly a tar file) that contains a bunch of software installed on top of a linux distribution.

```
# Pull alpine linux from dockerhub
user@machine:~/containerized-workshop/app$ docker pull alpine:3.6

# List available images
user@machine:~/containerized-workshop/app$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              3.6                 a41a7446062d        2 weeks ago         3.97MB
```

## Docker Container Part I
Images are cool because you can literally pack there yours app source code, environment variables, config files, software etc... However, it gets even better than that. You can interact with an image! A image that runs a process is called **container**. Other words, a container is a runtime instance of an image. Saying that lets get going.

```
# Lets run alpine linux image and install there some software.
# We will create hello.py script to verify that python works.
user@machine:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # apk update
/ # apk add python
/ # echo "print('docker rocks!')" > hello.py
/ # ls -l
/ # python hello.py
docker rocks!
```

You can check how many running containers is there by executing below command.
```
# Open new terminal and list running containers.
user@machine:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
878469647aa4        alpine:3.6          "/bin/sh"           About a minute ago   Up About a minute                       hardcore_swirles
```

To exit container press `Ctrl+D`

```
docker rocks! (Ctrl + D)
ludd@E7450:~/containerized-workshop/app$
```

Now lets run our image again (by running it we are creating a container) and lets execute our `hello.py` script that we created.

```
ludd@E7450:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # python hello.py
/bin/sh: python: not found
/ # ls-l
```

*"Houston we got a problem."* Didn't we install python and create `hello.py` script?. (Yes we did) So why is it gone? The reason is that images don't persist data (unless you put it there during build process). What actually happened is you run docker image for the second time and docker created a new container! Don't worry your data is there you just have to start `hardcore_swirles` container -I will show you how to do it.

### Docker Image Part II - Dockerfile
We discovered that our program is the *"real deal"* scientists love it, a monk opened a champaign and a vegan ate his first steak. Yee haa! I will build my own image. To do so follow below instruction.

```
ludd@E7450:~/containerized-workshop/app$ cd .
ludd@E7450:~/containerized-workshop$ touch Dockerfile
```

Fill Dockerfile (`~/containerized-workshop$/Dockerfile`) with below content.

```
FROM alpine:3.6

MAINTAINER Lukasz Dynowski ludd@cbs.dtu.dk

# Copy app dir form host into image
COPY ./app /app
WORKDIR /app

# Update packages
RUN apk update
RUN apk upgrade

# Install OS wide packages
RUN apk add bash
RUN apk add python
RUN apk add py-pip

# Install application wide packages
RUN pip install -r requirements.txt

# Execute script as a global program
RUN ln -s /app/main.py /usr/local/bin/fsa-analyzer
RUN chmod +x /usr/local/bin/fsa-analyzer

# Startup script
#CMD ["bash", "/app/scripts/startup.sh"]
```

To build and image execute this command.

```
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! Replace ldynia with your dockerhub username !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ludd@E7450:~/Coding/workshops/containerize$ docker build -t ldynia/conteneraized-workshop:1.0 .
Successfully built d80e90d300bc
Successfully tagged ldynia/conteneraized-workshop:1.0

ludd@E7450:~/Coding/workshops/containerize$ docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
ldynia/conteneraized-workshop   1.0                 d80e90d300bc        6 minutes ago       60.6MB

```

Lets run our image and see if our program works. At the same time open new terminal and write `docekr ps` while below program is executing. Run `docker ps` as well after the program is executed.

```
ludd@E7450:~/Coding/workshops/containerize$ docker run ldynia/conteneraized-workshop:1.0 fsa-analyzer /app/data/dna.fsa | python -m json.tool
{
    "nucleotides": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}
```

```
# While above program is running
ludd@E7450:~/Coding/workshops/containerize$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
db8b56d90a48        ldynia/conteneraized-workshop:1.0   "fsa-analyzer /app..."   2 seconds ago       Up 1 second                             happy_curran

# After program run
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
```
As you can container run for 5 sconds and was terminated at the moment when python stopped running. I will show you how to keep your containers up in **Program Part II**


## Docker Hub
To share your image with the whole world, you have to push it to [dockerhub](https://hub.docker.com).

```
# Login into your account
ludd@E7450:~/Coding/workshops/containerize$ docker login
Username (ldynia):
# Push image to dockerhub
ludd@E7450:~/Coding/workshops/containerize$ docker push ldynia/conteneraized-workshop:1.0
6c2769b873a4: Pushed
3854ae9c567b: Pushed
83b2e5750cd8: Pushed
2d791707ea0c: Pushed
5657379b46c0: Pushed
1c6ebc6ec0de: Pushed
4af3319f243b: Pushed
9b91d471feb9: Pushed
7f188a09b991: Pushed
3fb66f713c9f: Mounted from library/alpine
1.0: digest: sha256:f867cdf4ab69cecea051230a0ecf8d3880148a5f496c9bd5977d27e5ed8ed534 size: 2416
```

Now everyone in the world can download and run yours container.

```
# To pull image from dockerhub execute below command
ludd@E7450:~/Coding/workshops/containerize$ docker pull ldynia/conteneraized-workshop:1.0
```

## Program Part II
// TODO
// add infinity loop
// push for the second time
// Add docker compose
// volumes



# Singularity
