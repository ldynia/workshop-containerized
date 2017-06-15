# Containerized Workshop
This repository was created as a demo project to demonstrate usage of containerized technologies ([docker](https://docs.docker.com/) and [singularity](http://singularity.lbl.gov/)).

Objectives are to show scientists the beast practices using containerized technologies. You will learn how to package, distribute and share software using containerized technology.

# Docker
## Requirements
bellow requirements have to be full field.
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
Execute bellow instructions.

```
# Go to home directory
user@machine:~$ cd ~

# Clone repository
user@machine:~$ git clone https://github.com/ldynia/containerized-workshop

# Go to repository dir
user@machine:~$ cd containerized-workshop

# Remove these files
user@machine:~/containerized-workshop$ rm -rf composer-app.yml Dockerfile Singularityfile app/scripts/

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
Let's start with docker image first. Docker **image** is nothing more than a executable package (exactly a tar file) that contains a bunch of software installed on top of a Linux distribution.

```
# Pull alpine linux from dockerhub
user@machine:~/containerized-workshop/app$ docker pull alpine:3.6

# List available images
user@machine:~/containerized-workshop/app$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              3.6                 a41a7446062d        2 weeks ago         3.97MB
```

## Docker Container Part I
Images are cool because you can literally pack there yours app source code, environment variables, config files, software etc... However, it gets even better than that. You can interact with an image! A image that runs a process is called **container**. Other words, a container is a runtime instance of an image. Saying that let's get going.

```
# Let's run alpine linux image and install there some software.
# We will create hello.py script to verify that python works.
user@machine:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # apk update
/ # apk add python
/ # echo -e "#!/usr/bin/python \n\nprint('docker rocks!')" > hello.py
/ # ls -l
/ # python hello.py
/ # cat hello.py
/ # ln -s /hello.py /usr/local/bin/yo!
/ # chmod +x /usr/local/bin/yo!
docker rocks!
```

You can check how many running containers is there by executing bellow command.
```
# Open new terminal and list running containers.
user@machine:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
878469647aa4        alpine:3.6          "/bin/sh"           About a minute ago   Up About a minute                       hardcore_swirles
```

To exit a container press `Ctrl+D`

```
docker rocks! (Ctrl + D)
user@machine:~/containerized-workshop/app$
```

Let's run our image again (by running it we are creating a container) and Let's execute our `hello.py` script that we created.

```
user@machine:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # python hello.py
/bin/sh: python: not found
/ # ls-l
```

*"Houston we got a problem."* Didn't we install python and create `hello.py` script?. (Yes we did) So why is it gone? The reason is that images don't persist data (unless you put it there during build process). What actually happened is you run docker image for the second time and docker created a new container! Don't worry your data is there you just have to start `hardcore_swirles` container -I will show you how to do it.

## Docker Image Part II - Dockerfile
We discovered that our program is the *"real deal"* scientists love it, a monk opened a champaign and a vegan ate his first steak. Yee haa! I will build my own image. To do so follow bellow instruction.

```
user@machine:~/containerized-workshop/app$ cd .
user@machine:~/containerized-workshop$ touch Dockerfile
```

Fill Dockerfile (`~/containerized-workshop$/Dockerfile`) with bellow content.

```
# ~/containerized-workshop/Dockerfile
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
```

To build and image execute this command.

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! Replace ldynia with your dockerhub username !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

user@machine:~/containerized-workshop$ docker build -t ldynia/conteneraized-workshop:1.0 .
Successfully built d80e90d300bc
Successfully tagged ldynia/conteneraized-workshop:1.0

user@machine:~/containerized-workshop$ docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
ldynia/conteneraized-workshop   1.0                 d80e90d300bc        6 minutes ago       60.6MB
```

Let's run our image and see if our program works. At the same time open new terminal and write `docekr ps` while bellow program is executing. Run `docker ps` as well after the program is executed.

```
user@machine:~/containerized-workshop$ docker run ldynia/conteneraized-workshop:1.0 fsa-analyzer /app/data/dna.fsa | python -m json.tool
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
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
db8b56d90a48        ldynia/conteneraized-workshop:1.0   "fsa-analyzer /app..."   2 seconds ago       Up 1 second                             happy_curran

# After program run
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
```
As you can container run for 5 seconds and was terminated at the moment when python stopped running. I will show you how to keep your containers up in **Program Part II**


## Docker Hub
To share your image with the whole world, you have to push it to [dockerhub](https://hub.docker.com).

```
# Login into your account
user@machine:~/containerized-workshop$ docker login
Username (ldynia):
# Push image to dockerhub
user@machine:~/containerized-workshop$ docker push ldynia/conteneraized-workshop:1.0
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

Now everyone in the world can download your image and run it as a container.

```
# To pull image from dockerhub execute bellow command
user@machine:~/containerized-workshop$ docker pull ldynia/conteneraized-workshop:1.0
```

## Program Part II
Time passes image is a great success you got 2M+ downloads, and you decided to improve yours program.

Introduce bellow changes to your `~/containerized-workshop/app/main.py` file.

```
#time.sleep(5)

statistics = {
    'codons_count': stats.count_codons(),
    'nucleotides_count': stats.count_nucleotides(),
}
```

Create executable bash script `~/containerized-workshop/app/scripts/startup.sh`. This script will enforce container to stay up.

```
#!/bin/bash

# sleep infinity
echo "Starting infinity loop!"
while sleep 3600; do :; done
```

Add command at the end of `~/containerized-workshop/Dockerfile`. This command will execute startup script every time an image is run.
```
# Startup script
CMD ["bash", "/app/scripts/startup.sh"]
```

Let's build new image this image will include the recent changes that we made.

```
# Build new image
user@machine:~/containerized-workshop$ docker build -t ldynia/conteneraized-workshop:2.0 .
Successfully built c6fbaab9ba28
Successfully tagged ldynia/conteneraized-workshop:2.0
```

Let's test our new program.
```
# Run program
user@machine:~/containerized-workshop$ docker run ldynia/conteneraized-workshop:2.0 fsa-analyzer /app/data/dna.fsa | python -m json.tool
{
  "codons_count" : {
    "AAA": 8
    ...
    "TTT": 8
  },
  "nucleotides_count": {
      "A": 333,
      "C": 454,
      "G": 469,
      "T": 303
  }
}
```

Since our program works as expected we are ready to share it with the whole world again. Once it's uploaded everyone will be able to download it.

```
# Push program to dockerhub
user@machine:~/containerized-workshop$ docker push ldynia/conteneraized-workshop:2.0
```

Do you remember when I said about keeping the container up -thus we added `startup.sh` script. I will show you what I meant by that.


Open two terminal in one you will run images and in other you will display running containers.

**conteneraized-workshop:1.0**
```
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run -d ldynia/conteneraized-workshop:1.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND             CREATED                  STATUS                  PORTS               NAMES
a28dd7cecf80        ldynia/conteneraized-workshop:1.0   "/bin/sh"           Less than a second ago   Up Less than a second                       sad_kepler
```

**conteneraized-workshop:2.0**
```
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run -d ldynia/conteneraized-workshop:2.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
f3ddc0056c60        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   3 seconds ago       Up 2 seconds                            festive_galileo
```

Now you can see that `festive_galileo` (conteneraized-workshop:2.0) is up and running where, container `sad_kepler` (conteneraized-workshop:1.0) was exited straight after execution.

## Docker Container Part II

There are some advantages of keeping containers up and running. One of it's that containers persist data -*removing container == deleting data withing a container*. Another is, that you can interact with container as if you were interacting with an image. Remember a container is running instance of and image. As my collage said *"if an image is a class then a container is an object"*

Interacting with a container is like interacting with an image. The best illustration is comparing bellow commands

```
# Run fsa-analyzer against the image
user@machine:~/containerized-workshop$ docker run ldynia/conteneraized-workshop:1.0 fsa-analyzer /app/data/dna.fsa

# Run fsa-analyzer against the container
user@machine:~/containerized-workshop$ docker exec festive_galileo fsa-analyzer /app/data/dna.fsa
```

## Docker Volumes
Even thought our program kicks asses and nerds go crazy about it -since it was mentioned in science. There is a serious draw back. Namely, it can analyze only one file -being precise file located in the container. This is where volumes come with help. **Volume** is a bridge (mount) that connects yours machine files system (host) with the container. Enough, talking let's create our first volume.

Let's create new data directory (`data-x`) and fsa file (`rsa.fsa`).

```
user@machine:~/containerized-workshop$ cd app/
user@machine:~/containerized-workshop/app$ cp -r data/ data-x/
user@machine:~/containerized-workshop/app$ cd data-x
user@machine:~/containerized-workshop/app/data-x$ mv dna.fsa rna.fsa
user@machine:~/containerized-workshop/app/data-x$ cd ../..
user@machine:~/containerized-workshop$ docker run -d --name demo -v $(pwd)/app/data-x:/data-x ldynia/conteneraized-workshop:2.0
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED              STATUS              PORTS               NAMES
3da8ba3b7fb4        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   About a minute ago   Up About a minute                       demo


user@machine:~/containerized-workshop$ docker exec -it demo fsa-analyzer /app/data-x/rna.fsa | python -m json.tool
{
    "codons": {
        "AAA": 8,
        ....
        "TTT": 8
    },
    "nucleotides": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}

user@machine:~/containerized-workshop$ docker stop demo
user@machine:~/containerized-workshop$ docker container prune
```


## Docker compose
I have to admit that writing in terminal long executable commands with full of flags the last thing that I wont to read and write! If you share my pain then there is a solution. What if I told you that you could do all this terminal mambo-jumob with a one file and one command? Excited, than let's have a look at `docker-compose`.

Let's create docker-compose file `~/containerized-workshop/composer-app.yml` and copy-paste bellow content.

```
# ~/containerized-workshop/compose-app.yml
version: '3'

services:

  application:
    image: ldynia/conteneraized-workshop:2.0
    build: .
    restart: always
    container_name: demo
    volumes:
      - ./app:/app
    environment:
      MAGIC: abbracadabbra
    command: bash scripts/startup.sh
```

Once our docker-compose file is create let's run it.

```
# Run docker-compose. You can -d at the end to run container in detach mode
user@machine:~/containerized-workshop$ docker-compose -f composer-app.yml up
Creating demo ...
Creating demo ... done
Attaching to demo
demo           | Starting infinity loop!
```

Open new terminal and check that it works.

```
user@machine:~/containerized-workshop$ docker ps
user@machine:~/containerized-workshop$ docker exec -it demo fsa-analyzer /app/data-x/rna.fsa | python -m json.tool
{
    "nucleotides_count": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}
```


# Singularity
Even thought Docekr rocks! There are some aspects of it (due to its implementation) that will not make docker not necessary the best tool for a scientist need. [Singularity](http://singularity.lbl.gov/), is another containerized solution that addresses similar problems with different approach. The best part of it's that it utilizes docker images :) You will be astonished how simple it's to containerize your application (software) into it.


Objectives are the same to package, and distribute our awesome program this time using singularity image.


## Installation
Depending on yours OS distribution please follow installation guide [install](http://singularity.lbl.gov/release-2-3). To verify that singularity is installed to as below.

```
user@machine:~/containerized-workshop$ singularity --version
2.3-dist
```

## Image

Let's create our first singularity image.

```
# Create an image
user@machine:~/containerized-workshop$ singularity create alpine.img
Initializing Singularity image subsystem
Opening image file: alpine.img
Creating 768MiB image
Binding image to loop
Creating file system within image
Image is done: alpine.img

# Check image size 769MB
user@machine:~/containerized-workshop$ ls -lh alpine.img
-rwxr-xr-x 1 ludd ludd 769M Jun 15 15:07 alpine.img

# Check image size again 29MB
user@machine:~/containerized-workshop$ du -h alpine.img
29M	alpine.img

# Import docker's alpine image into our singularity image
user@machine:~/containerized-workshop$ singularity import alpine.img docker://alpine:3.6
Docker image path: index.docker.io/library/alpine:3.6
Cache folder set to /home/ludd/.singularity/docker
[1/1] |===================================| 100.0%
Importing: base Singularity environment
Importing: /home/ludd/.singularity/docker/sha256:d5e46245fe40c2d1ab72bfe328de28549b605b2587ab2fa8715f54e3e2de9c5d.tar.gz
Importing: /home/ludd/.singularity/metadata/sha256:6b8bbe197a20c88d065c265cf6f6f8b4e3695f104d1f47f01a1298b3566f27fe.tar.gz

# Check image size again
user@machine:~/containerized-workshop$ du -h alpine.img
33	alpine.img
```

Once image is created we can interact with it.

```
# Shell into image
user@machine:~/containerized-workshop$ singularity shell alpine.img
Singularity: Invoking an interactive shell within container...

# Check usernaem
Singularity alpine.img:~/Coding/workshops/containerize/singularity> whoami
user

# Update repository list
Singularity alpine.img:~/Coding/workshops/containerize/singularity> apk update
Loaded plugins: fastestmirror, ovl
ovl: Error while doing RPMdb copy-up:
[Errno 13] Permission denied: '/var/lib/rpm/Installtid'
You need to be root to perform this command.
Singularity alpine.img:~/Coding/workshops/containerize/singularity> exit

# Login as a root
user@machine:~/containerized-workshop$ sudo singularity shell alpine.img
Singularity: Invoking an interactive shell within container...

Singularity alpine.img:~> whoami
root

# Update repositories
Singularity alpine.img:~> apk update
ERROR: Unable to lock database: Permission denied
ERROR: Failed to open apk database: Permission denied
```

## Writeing into an image
As you can see singularity is very strict to who can interact with an image and what can be written there.

To write into an image just add `--writable` flag.

```
# Login as a sudo in writable mode
user@machine:~/containerized-workshop$ sudo singularity shell --writable alpine.img
Singularity: Invoking an interactive shell within container...

Singularity alpine.img:~> apk update
Singularity alpine.img:~> apk add git
Singularity alpine.img:~> apk add vim
Singularity alpine.img:~> exit

user@machine:~/containerized-workshop$ sudo singularity shell alpine.img
Singularity alpine.img:~> vim
Singularity alpine.img:~> exit
```

## Singularity file
We know that it's a bit of a hassle to do everything from terminal. Fortunately, we can automatize our work and create singularity bootstrap file which is equivalent to a Dockerfile.

Create Singularity file and copy-paste bellow content into it.
```
# Singularityfile bootstrap file
# ~/containerized-workshop/Singularityfile
Bootstrap: docker
From: alpine:3.6

%runscript

exec echo "The runscript is the containers default runtime command!"

%labels
AUTHOR ludd@cbs.dtu.dk

%post

# Install packages
apk update
apk add git
apk add bash
apk add python
apk add py-pip

# Clone git repo and remove git repo
git clone https://github.com/ldynia/containerized-workshop
mv /containerized-workshop/app /app
rm -rf /containerized-workshop

# Execute script as a global program
ln -s /app/main.py /usr/local/bin/fsa-analyzer
chmod +x /usr/local/bin/fsa-analyzer

echo "The post section is where you can install, and configure your container."
```

Once file is created then we will build image from it.
```
# Recreate alpine image
user@machine:~/containerized-workshop$ rm alpine.img
user@machine:~/containerized-workshop$ singularity create alpine.img

# Bootstrap image from file
user@machine:~/containerized-workshop$ sudo singularity bootstrap alpine.img Singularityfile

# Check if it works!
user@machine:~/containerized-workshop$ singularity exec alpine.img fsa-analyzer /app/data/dna.fsa
{"nucleotides": {"A": 333, "C": 454, "T": 303, "G": 469}}
```

## Distribute an image

Send it via email, copy it on usb stick or upload to cloud -you name it!, and deliver it to person that you want to share file with.
