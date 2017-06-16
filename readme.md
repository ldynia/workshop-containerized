# Containerized Workshop
This repository was created as a demo project to demonstrate usage of containerized technologies ([docker](https://docs.docker.com/) and [singularity](http://singularity.lbl.gov/)). Audience of this project are scientists, phds, developer who build tools (software) and would like to share it and suport validation of scientific papers by validating it in a reproducible way.

Aim of this project is to teach audience the best practices on how to package, distribute and share software with containerized technologies.

# Docker
## Requirements
Bellow requirements have to be full field.
* [git](https://git-scm.com/downloads) - installed
* [docker](https://docs.docker.com/) - installed
* [dockerhub](https://hub.docker.com/) account
* [docker-compose](https://docs.docker.com/compose/install/#alternative-install-options) account
* [pytohn](https://www.python.org/downloads/) -installed
* [pip](https://pypi.python.org/pypi/pip) -installed
* [singularity](http://singularity.lbl.gov/) -installed
* sudo/root access yours machine

**Check**
```
# Check if docker service is running
user@machine:~$ sudo service docker status
[sudo] password for user:
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2017-06-13 16:41:02 CEST; 21h ago


# Check if user belongs to docker group
user@machine:~$ groups
adm sudo staff users vboxusers docker

# Check if user belongs to docker group
user@machine:~$ groups
adm sudo staff users vboxusers docker

# Check if singularit is installed
user@machine:~/containerized-workshop$ singularity --version
2.3-dist
```


## Git
Execute bellow instructions.

```
# Go to home directory
user@machine:~$ cd ~

# Clone project's repository
user@machine:~$ git clone https://github.com/ldynia/containerized-workshop

# Go to project's dir
user@machine:~$ cd containerized-workshop

# Remove these files
user@machine:~/containerized-workshop$ rm -rf composer-app.yml Dockerfile Singularityfile app/scripts/

```
## Program - Part I
Let me introduce you to a program that saves lives. The program is very simple. Input of the program is `*.fsa` file. Output of the program is count of nucleotides and codons that were found in a `*fsa` file. **Note:** Program returns output after 5s -this is an intended behavior.

To see how our program works please execute bellow instructions.
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

## Docker Image - Part I
Let's start with the definition of an **IMAGE** file. An image is an **executable file (tar file or sparse file) that contains a bunch of tools (software), environment variables, configuration files, source code installed on top of a Linux distribution**.

Let's download our first docker image :)
```
# Pull alpine linux image from dockerhub
user@machine:~/containerized-workshop/app$ docker pull alpine:3.6

# List all available images
user@machine:~/containerized-workshop/app$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              3.6                 a41a7446062d        2 weeks ago         3.97MB
```

## Docker Container - Part I
Notion of image is cool because you can literally pack into it your's tools such as, source code, config files, other software etc... However, it gets even better than that. You can interact with an image!


 An image that runs a process is called **CONTAINER**. Other words, a container is a **runtime instance of an image**.

 Saying that let's get going.

```
# Let's run image with alpine distribution, and install there python.
# After installation we will create hello.py script to verify that python works.
user@machine:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # apk update
/ # apk add python
/ # echo -e "#!/usr/bin/python \n\nprint('docker rocks!')" > hello.py
/ # ls -l
/ # python hello.py
/ # cat hello.py
/ # ln -s /hello.py /usr/local/bin/yo!
/ # chmod +x /usr/local/bin/yo!
/ # yo!
docker rocks!
```

At any time you can check how many running containers docker is running. You will see that a container has a name (*hardcore_swirles*) and is associated with the image.
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

We will run our image again and we will execute our `hello.py` again.

```
user@machine:~/containerized-workshop/app$ docker run -it alpine:3.6
/ # python hello.py
/bin/sh: python: not found
/ # ls-l
```

*"Houston we got a problem."* Didn't we install python and create `hello.py` script?. (Yes we did) So why is it gone? The reason is that images don't persist data (unless you put it there during build process). What actually happened is we run docker image for the second time and docker created a new container! Don't worry your data is there you just have to run our `yo!` program against `hardcore_swirles` container.


```
# Run yo! programm against docekr container
user@machine:~/containerized-workshop/app$ docker exec hardcore_swirles yo!
docker rocks!
```


## Docker Image - Part II - Dockerfile
We discovered that our program is the *"real deal"* scientists love it, a monk opened a champaign and a vegan ate his first steak. ([Leeroy Jenkins!!!!](https://www.youtube.com/watch?v=hooKVstzbz0))
It is fun to run someone else's images but, it is even cooler to build own image. Let's build one by flollowing bellow instructions.

```
user@machine:~/containerized-workshop/app$ cd ..
user@machine:~/containerized-workshop$ touch Dockerfile
```

Enter bellow content into `Dockerfile`.

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

To build and image execute this command. **Replace *ldynia* with your dockerhub username!!!**

```
# Build docker image with Dockerfile
user@machine:~/containerized-workshop$ docker build -t ldynia/conteneraized-workshop:1.0 .
Successfully built d80e90d300bc
Successfully tagged ldynia/conteneraized-workshop:1.0

# Display available images
user@machine:~/containerized-workshop$ docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
alpine                          3.6                 a41a7446062d        2 weeks ago         3.97MB
ldynia/conteneraized-workshop   1.0                 d80e90d300bc        6 minutes ago       60.6MB
```

Let's run our newly created image and see if the program works. At the same time when program is running open a new terminal and execute `docekr ps` command. Execute dockere `docker ps` once more after the program is ended.

```
# Run our program
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
# While our program is running execute `docker ps`
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
db8b56d90a48        ldynia/conteneraized-workshop:1.0   "fsa-analyzer /app..."   2 seconds ago       Up 1 second                             sharp_brown

# After program prodiced output run `docker ps` again
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
```
As you can see our *sharp_brown* container was visable for 5 seconds and disappeared right after our program ended. There is a way how to keep container up (running) and I will show you how to do it in **Program - Part II**

## Docker Hub
Since we agree that our program is a "break throught" in scientific world we will share it. To share your image with the whole world, you have to push it to [dockerhub](https://hub.docker.com) (you need to have an account there).

```
# Login into your account
user@machine:~/containerized-workshop$ docker login
Username (ldynia):

# Push tagged image to dockerhub
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
# Remove image from your machine
user@machine:~/containerized-workshop$ docker rmi -f ldynia/conteneraized-workshop:1.0

# To pull image from dockerhub execute bellow command
user@machine:~/containerized-workshop$ docker pull ldynia/conteneraized-workshop:1.0
```

## Program - Part II
Time passes image is a great success you got 2M+ downloads per day and we decided to improve our's program.

Let's introduce bellow changes to your `main.py` file.

```
## ~/containerized-workshop/app/main.py
time.sleep(5)

statistics = {
    'codons_count': stats.count_codons(),
    'nucleotides_count': stats.count_nucleotides(),
}
```

We will as well create an executable bash script that will enforce container to stay up `~/containerized-workshop/app/scripts/startup.sh`.

```
#!/bin/bash

# sleep infinity
echo "Starting infinity loop!"
while sleep 3600; do :; done
```

As well we have to add command at the end of `Dockerfile`. This command will execute startup script every time an image is run.
```
## ~/containerized-workshop/Dockerfile

# Startup script
CMD ["bash", "/app/scripts/startup.sh"]
```

Let's build new image.
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

Since our program works as expected we are ready to share it with the whole world again -so everyone will be able to download new version.

```
# Tag the image and push it to dockerhub
user@machine:~/containerized-workshop$ docker push ldynia/conteneraized-workshop:2.0
```

Do you remember what I said about keeping a container up (running)? To keep container up we created  `startup.sh` script that will be executed ecery time when an image is run. Let's see what I mean.


Let's open two terminals. In one termianl you will run image and in other you will display running images (containers).

**conteneraized-workshop:1.0**
```
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run --name container1.0 -d ldynia/conteneraized-workshop:1.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND             CREATED                  STATUS                  PORTS               NAMES
a28dd7cecf80        ldynia/conteneraized-workshop:1.0   "/bin/sh"           Less than a second ago   Up Less than a second                      container1.0
```

**conteneraized-workshop:2.0**
```
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run -d --name container2.0 ldynia/conteneraized-workshop:2.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
f3ddc0056c60        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   3 seconds ago       Up 2 seconds                            container2.0
```

Now you can see that `container2.0` (conteneraized-workshop:2.0) is up and running where, container `container1.0` (conteneraized-workshop:1.0) was exited straight after execution.

## Docker Container - Part II

There are some advantages of keeping containers up and running. One of it's that containers persist data -*removing container == deleting data within a container*. Another is, that you can interact with container as if you were interacting with an image.

Remember taht a container is running instance of the image. As my collage said in Object Oriented way *"if an image is a class then a container is an object"*

Interacting with a container is just like interacting with an image. Compare bellow commadns.

```
# Run fsa-analyzer against the image
user@machine:~/containerized-workshop$ docker run ldynia/conteneraized-workshop:1.0 fsa-analyzer /app/data/dna.fsa

# Run fsa-analyzer against the container
user@machine:~/containerized-workshop$ docker exec container2.0 fsa-analyzer /app/data/dna.fsa
```

## Docker Volumes
Even thought our program kicks asses and nerds go crazy about it -since it was mentioned in the [science](http://www.sciencemag.org/). There is a serious draw back. Namely, it can analyze only one file (the file located in the container). This is where volumes come with help. **Volume** is a **bridge (mount) that connects yours machine files system (host) with the container**.

Enough, talking let's create our first volume. First, we have to create new data directory (`data-x`) and fsa file (`rsa.fsa`).

```
user@machine:~/containerized-workshop$ cd app/
user@machine:~/containerized-workshop/app$ cp -r data/ data-x/
user@machine:~/containerized-workshop/app$ cd data-x
user@machine:~/containerized-workshop/app/data-x$ mv dna.fsa rna.fsa
user@machine:~/containerized-workshop/app/data-x$ cd ../..
user@machine:~/containerized-workshop$ docker run -d --name playground -v $(pwd)/app/data-x:/data-x ldynia/conteneraized-workshop:2.0
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED              STATUS              PORTS               NAMES
3da8ba3b7fb4        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   About a minute ago   Up About a minute                       playground


user@machine:~/containerized-workshop$ docker exec -it playground fsa-analyzer /app/data-x/rna.fsa | python -m json.tool
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

user@machine:~/containerized-workshop$ docker stop playground
user@machine:~/containerized-workshop$ docker container prune
```


## Docker compose
I have to admit that writing in a terminal long executable commands with full of flags is the last thing that I want to do! If you share my pain then there is the solution. What if I told you that you could do all this terminal mambo-jumob with a one file and one command excited?, Here is where `docker-compose` comes to play.

Let's create a docker-compose file `composer-app.yml` and copy-paste bellow content.

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
Even thought Docekr rocks! There are some aspects of it (due to its implementation) that will not make docker the best solution for your needs.

[Singularity](http://singularity.lbl.gov/), is another containerized solution that addresses similar problems with different approach. The best part of it's that it utilizes docker images :) You will be astonished how simple it's to containerize your application (software) into it.


In this section we will do exactly the same with singularity what we did with docker.

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
