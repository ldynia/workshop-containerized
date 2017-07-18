# Containerized Workshop

This repository is a tutorial created to demonstrates usage of containerized technologies. The technologies that I am referring to are [docker](https://docs.docker.com/) and [singularity](http://singularity.lbl.gov/).

Audience of this project are scientists, phds, developers who build software (tools). Containerized technologies allows scientist (developers) to packages, interact and distribute their's software. Consequences of this practice are that results of a scientific paper can be reproducible.

Aim of this project is to teach the audience the best practices on how to use containerized technologies. After finishing this tutorial you will know how to package, distribute and share yours software (tools) using [docker](https://docs.docker.com/) and [singularity](http://singularity.lbl.gov/).

# Docker

## Requirements

Before you start tutorial you have to fulfilled below requirements.

- [git](https://git-scm.com/downloads) - installed
- [docker](https://docs.docker.com/) - installed
- [dockerhub](https://hub.docker.com/) account
- [docker-compose](https://docs.docker.com/compose/install/#alternative-install-options) account
- [pytohn](https://www.python.org/downloads/) -installed
- [pip](https://pypi.python.org/pypi/pip) -installed
- [singularity](http://singularity.lbl.gov/) -installed
- sudo/root access yours machine

## Assumption

Workshop base on the assumption that all points in requirements are fulfilled.

## Git

Let's start with cloning this repository to yours computer. Because repository is a complete solution we will have to delete some files -don't worry we will recreate them as we proceed with the tutorial.

Please execute bellow instructions.
```Bash
# Go to home directory
user@machine:~$ cd ~

# Clone project's repository
user@machine:~$ git clone https://github.com/ldynia/containerized-workshop

# Go to project's dir
user@machine:~$ cd containerized-workshop

# Remove these files
user@machine:~/containerized-workshop$ rm -rf docker-compose.yml Dockerfile Singularityfile app/scripts/
```

## Program - Part I

Let me introduce you to our program -we will call it `fsa-analyzer`. The program is very simple and works like this. The program takes as an input a `*.fsa` file, and returns count of nucleotides. **Note:** The program returns output after 5 seconds -this is an intended behavior.

To see how our program works please execute bellow instructions.

```Bash
# Go to app directory
user@machine:~/containerized-workshop$ cd app

# Run program
user@machine:~/containerized-workshop/app$ python main.py data/dna.fsa
{"nucleotides_count": {"A": 333, "C": 454, "T": 303, "G": 469}}

# Or run program and pritify its output
user@machine:~/containerized-workshop/app$ python main.py data/dna.fsa | python -m json.tool
{
    "nucleotides": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}

# Go back to containerized-workshop directory
user@machine:~/containerized-workshop/app$ cd ..
```

## Docker Image - Part I

Let's start with the definition of an **IMAGE** file. An image is an **executable file (tar file or sparse file) that contains a bunch of tools (software), environment variables, configuration files, source code installed on top of a Linux distribution**. I think of an image as it was a blueprint of a house -with one blueprint you can build infinite number of houses.

Let's download first docker image. The image that we will download will be the image with Alpine Linux distribution.

```Bash
# Pull alpine linux image from dockerhub
user@machine:~/containerized-workshop$ docker pull alpine:3.6

# List all available images
user@machine:~/containerized-workshop$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              3.6                 a41a7446062d        2 weeks ago         3.97MB
```

## Docker Container - Part I

An image that runs a process is called **CONTAINER**. Other words, a container is a **runtime instance of an image**. I think of a container as it was a real house -a place where you can get it and start furnishing it.

A container is an awesome thing. You can literally pack into it your source code, config files, data files, other software, etc... and it will persist those data. On the other hand an image once is created (build) it will not persist data. **Remember an image is the blueprint a container is the real thing!**

Saying that let's get going, and let's create our first container.

```Bash
# Let's run downloaded image, and let's install python there.
# After installation we will create hello.py script to verify that python works.
user@machine:~/containerized-workshop$ docker run -it alpine:3.6
/ # apk update
/ # apk add python
/ # echo -e "#!/usr/bin/python \n\nprint('docker rocks!')" > hello.py
/ # ls -l
/ # python hello.py
/ # ln -s /hello.py /usr/local/bin/yo!
/ # chmod +x /usr/local/bin/yo!
/ # yo!
docker rocks!
```


Remember that ran image is called **container**. At any time you can check how many containers docker is running with `docker ps` command. You will see that a container has an id, a name (*angry_swanson*) and image associated with it, as well as other information.

```Bash
# Open new terminal and list running containers.
user@machine:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
878469647aa4        alpine:3.6          "/bin/sh"           About a minute ago   Up About a minute                       angry_swanson
```

To exit our container press `Ctrl+D`

```Bash
docker rocks! (Ctrl + D)
user@machine:~/containerized-workshop$
```

With `Ctrl + D` we exited (and stopped) *angry_swanson* container. So let's check if our container is running. To do that we will execute `docker ps` again.

```Bash
# List all running containers
user@machine:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
```

No surprises there. The question is what happened to the container. Was it deleted with the moment when we stopped it? Was it abducted by aliens? and finally was 9.11 an inside job?

Being serious, to see stopped containers execute bellow command.

```Bash
# List all stopped containers
user@machine:~/containerized-workshop$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
878469647aa4        alpine:3.6          "/bin/sh"           About an hour ago   Exited (0) 40 minutes ago                       angry_swanson
```

As we can see *angry_swanson* is still there and it was not deleted. The question is can we bring back to live and run our `yo!` program? Yes we can, to start a container execute bellow command.

```Bash
# Start container
user@machine:~/containerized-workshop$ docker start angry_swanson

# List all running containers
user@machine:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
878469647aa4        alpine:3.6          "/bin/sh"           About an hour ago   Up 4 minutes                            angry_swanson
```

Container are awesome because you can interact with them. To interact with a container you use `exec` command. Let's exec our `yo!` program again.

```Bash
# Run yo! program against docker container
user@machine:~/containerized-workshop$ docker exec angry_swanson yo!
docker rocks!
```

Remember that exec works only with running container. Let's see what will happened when we will stop a container.

```Bash
# Stop container
user@machine:~/containerized-workshop$ docker stop angry_swanson

# Run exec against stopped container
user@machine:~/containerized-workshop$ docker exec angry_swanson yo!
Error response from daemon: Container 878469647aa4611b36de1f97a8e9d1273fbeb228ac355777e4e1b02e118fa272 is not running
```

The best part about containers is that can hook into it. Let me demonstrate.

```Bash
# Start angry_swanson again
user@machine:~/containerized-workshop$ docker start angry_swanson

# Hook in into container
user@machine:~/containerized-workshop$ docker exec -it angry_swanson sh
/ # ls -l
total 56
drwxr-xr-x    2 root     root          4096 May 25 15:18 bin
drwxr-xr-x    5 root     root           360 Jun 17 18:52 dev
drwxr-xr-x   16 root     root          4096 Jun 17 17:52 etc
-rwxr-xr-x    1 root     root            43 Jun 17 17:52 hello.py
drwxr-xr-x    2 root     root          4096 May 25 15:18 home
drwxr-xr-x    6 root     root          4096 Jun 17 17:52 lib
drwxr-xr-x    5 root     root          4096 May 25 15:18 media
drwxr-xr-x    2 root     root          4096 May 25 15:18 mnt
dr-xr-xr-x  289 root     root             0 Jun 17 18:52 proc
drwx------    2 root     root          4096 Jun 17 17:52 root
drwxr-xr-x    2 root     root          4096 May 25 15:18 run
drwxr-xr-x    2 root     root          4096 May 25 15:18 sbin
drwxr-xr-x    2 root     root          4096 May 25 15:18 srv
dr-xr-xr-x   13 root     root             0 Jun 17 18:52 sys
drwxrwxrwt    2 root     root          4096 May 25 15:18 tmp
drwxr-xr-x   12 root     root          4096 Jun 17 17:53 usr
drwxr-xr-x   13 root     root          4096 Jun 17 17:52 var
/ # top
Mem: 4979744K used, 3105372K free, 482628K shrd, 852336K buff, 1532500K cached
CPU:   0% usr   0% sys   0% nic  87% idle  12% io   0% irq   0% sirq
Load average: 0.22 0.50 0.68 2/853 53
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     S     1544   0%   2   0% /bin/sh
   31     0 root     S     1544   0%   0   0% sh
   44     0 root     S     1544   0%   2   0% sh
   53    44 root     R     1536   0%   7   0% top
   25     0 root     S     1532   0%   5   0% sh
```

Notice that only few processes are running inside our container (Alpine Linux). It's because container's processes are isolated from the system processes.

## Docker Image - Part II - Dockerfile

Going back to our `fsa-analyzer`. Suddenly, we discovered that our program is the *"real deal"* scientists love it, a monk opened a champaign and, a vegan ate his first steak. ([Leeroy Jenkins!!!!](https://www.youtube.com/watch?v=hooKVstzbz0)).

We decided to create our own image and we will pack there our program. To make our program running we need 3 things. Source code (checked), operating system (checked -Alpine Linux), Python (not checked).

To build an image you have to create a `Dockerfile` (the blueprint file). This file will contain set of instructions executed line by line from top to bottom.

Crate a `Dockerfile`

```Bash
user@machine:~/containerized-workshop$ touch Dockerfile
```

Enter bellow content into `Dockerfile`.

```Bash
# ~/containerized-workshop/Dockerfile
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
```

To build and image from a `Dockerfile` execute bellow command. **Replace _ldynia_ with your dockerhub username !!!**

```Bash
# Build docker image with Dockerfile
user@machine:~/containerized-workshop$ docker build -t ldynia/conteneraized-workshop:1.0 .
Successfully built d80e90d300bc
Successfully tagged ldynia/conteneraized-workshop:1.0

# Display available images
user@machine:~/containerized-workshop$ docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
alpine                          3.6                 a41a7446062d        2 weeks ago         3.97MB
ldynia/conteneraized-workshop   1.0                 d80e90d300bc        6 minutes ago       59.7MB
```

Let's crate a container from our newly created image and see if our program works. At the same time when program is running open a new terminal and execute `docker ps` command. Execute docker `docker ps` once more after the program is ended.

```Bash
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

```Bash
# While our program is running execute `docker ps`
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
db8b56d90a48        ldynia/conteneraized-workshop:1.0   "fsa-analyzer /app..."   2 seconds ago       Up 1 second                             sharp_brown
878469647aa4        alpine:3.6                          "/bin/sh"                2 hours ago         Up 24 seconds                           angry_swanson

# After program prodiced output run `docker ps` again
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
878469647aa4        alpine:3.6                          "/bin/sh"                2 hours ago         Up 24 seconds                           angry_swanson
```

As you can see our *sharp_brown* container was visible for 5 seconds and disappeared right after our program ended. There is a way to keep container up (running) and I will show you how to do it in **Program - Part II**

## Docker Hub

Our program is a "break through" in scientific world and we decided to share it. To share your image with the whole world, you have to push it to [dockerhub](https://hub.docker.com) (you need to have an account there).

```Bash
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

```Bash
# Remove image from your machine
user@machine:~/containerized-workshop$ docker rmi -f ldynia/conteneraized-workshop:1.0

# To pull image from dockerhub execute bellow command
user@machine:~/containerized-workshop$ docker pull ldynia/conteneraized-workshop:1.0

# Let's remove unused containers
user@machine:~/containerized-workshop$ docker container prune
```

## Program - Part II

Time passes, our image is a great success you got 2M+ downloads per day and we decided to improve `fsa-analyzer`.

Let's introduce bellow changes to `main.py` file.

```Bash
## ~/containerized-workshop/app/main.py
#time.sleep(5)

statistics = {
    'codons_count': stats.count_codons(),
    'nucleotides_count': stats.count_nucleotides(),
}
```

As well we will create an executable bash script that will enforce container to stay up and running. Create this file `~/containerized-workshop/app/scripts/startup.sh`.

```Bash
#!/bin/bash

# sleep infinity
echo "Starting infinity loop!"
while sleep 3600; do :; done
```

Additionally, we have to add a command at the end of our `Dockerfile`. This command will execute startup script every time an image is run.

```Bash
# Startup script
CMD ["sh", "/app/scripts/startup.sh"]
```

Let's build new image.

```
# Build new image
user@machine:~/containerized-workshop$ docker build -t ldynia/conteneraized-workshop:2.0 .
Successfully built c6fbaab9ba28
Successfully tagged ldynia/conteneraized-workshop:2.0
```

Let's test our new program.

```Bash
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

Since our updated program works as expected, we will share it with the whole world again.

```Bash
# Tag the image and push it to dockerhub
user@machine:~/containerized-workshop$ docker push ldynia/conteneraized-workshop:2.0
```

Do you remember what I said about keeping a container up (running)? To keep container up we created `startup.sh` script that will be executed every time when our image is run. Let's see what I mean by that.

Let's open two terminals. In one terminal we will create a container with `docker run` command. In other terminal we will display running containers with `docker ps`.

**conteneraized-workshop:1.0**

```Bash
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run -d --name container1.0 ldynia/conteneraized-workshop:1.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND             CREATED                  STATUS                  PORTS               NAMES
a28dd7cecf80        ldynia/conteneraized-workshop:1.0   "/bin/sh"           Less than a second ago   Up Less than a second                      container1.0
```

**conteneraized-workshop:2.0**

```Bash
# Run image detach -in first terminal
user@machine:~/containerized-workshop$ docker run -d --name container2.0 ldynia/conteneraized-workshop:2.0

# Display running containers in second terminal
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
f3ddc0056c60        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   3 seconds ago       Up 2 seconds                            container2.0
```

You can see that `container2.0` is up and running where, container `container1.0` was exited straight after execution.

## Docker Container - Part II

There are some advantages of keeping containers up and running. One of it's that containers persist data -*removing container equals to deleting data*. Another is, that you can interact with container as if you were interacting with an image.

Remember that a container is running instance of the image. As my collage said in Object Oriented way *"if an image is a class then a container is an object"*

We used `docekr run` to interact with an image. To interact with a container we use `docker exec`

```Bash
# Run fsa-analyzer against running container
user@machine:~/containerized-workshop$ docker exec container2.0 fsa-analyzer /app/data/dna.fsa
```

## Docker Volumes

Even thought our program kicks asses and *"nerds"* go crazy about it -since it was mentioned in the [science](http://www.sciencemag.org/). There is a serious draw back. Namely, it can analyze only one file (the file that we copied when we builded our image). This is where volumes come with help. **Volume** is a **bridge that connects yours machine files system with the container**.

Enough talking let's create a volume. To demonstrate that volumes works we will create new directory (`data-x`) and fsa file (`rsa.fsa`).

```Bash
# Create dummy data
user@machine:~/containerized-workshop$ cd app/
user@machine:~/containerized-workshop/app$ cp -r data/ data-x/
user@machine:~/containerized-workshop/app$ cd data-x
user@machine:~/containerized-workshop/app/data-x$ mv dna.fsa rna.fsa
user@machine:~/containerized-workshop/app/data-x$ cd ../..

# Add volume to image/container
user@machine:~/containerized-workshop$ docker run -d --name playground -v $(pwd)/app/data-x:/data-x ldynia/conteneraized-workshop:2.0
user@machine:~/containerized-workshop$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED              STATUS              PORTS               NAMES
3da8ba3b7fb4        ldynia/conteneraized-workshop:2.0   "bash /app/scripts..."   About a minute ago   Up About a minute                       playground

# Check if our volume works
user@machine:~/containerized-workshop$ docker exec playground fsa-analyzer /data-x/rna.fsa | python -m json.tool
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
```

## Docker compose

I have to admit that, writing long executable commands full of flags in terminal is the last thing that I want to do! If you share my pain then there is a solution for it. What if I told you that you could do all this terminal *mambo-jumob* with a one file and one command excited?, Here is where `docker-compose` comes to play.

Let's create a docker-compose file `docker-compose.yml` and copy-paste bellow content.

```
# ~/containerized-workshop/docker-compose.yml
version: '3'

services:

  application:
    image: ldynia/conteneraized-workshop:2.0
    build: .
    restart: always
    container_name: demo
    volumes:
      - ./app/data-x:/data-x
    environment:
      MAGIC: abbracadabbra
    command: sh scripts/startup.sh
```

Once our docker-compose file is create let's run it.

```Bash
# Run docker-compose in detach mode
user@machine:~/containerized-workshop$ docker-compose up -d
Creating demo ...
Creating demo ... done

# Execute fsa-analyzer to check if everrything is working
user@machine:~/containerized-workshop$ docker exec demo fsa-analyzer /data-x/rna.fsa | python -m json.tool
{
    "nucleotides_count": {
        "A": 333,
        "C": 454,
        "G": 469,
        "T": 303
    }
}

# Stop container with docker-compose
user@machine:~/containerized-workshop$ docker-compose stop
Stopping demo ... done
```

# Singularity

Even thought docker rocks! There are some aspects of it (due to its implementation) that will not make docker the best solution for yours needs.

[Singularity](http://singularity.lbl.gov/), is another containerized solution that addresses similar problems as docker but, with different approach. The best part of it's that it utilizes docker images :) You will be astonished how simple it's to containerize your application (software).

In this section we will package our `fsa-analyzer` into a singularity image.

## Image

Let's create our first singularity image.

```Bash
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
29M    alpine.img

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
33    alpine.img
```

Once image is created we can interact with it.

```Bash
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
ERROR: busybox-1.26.2-r4.trigger: failed to execute: No space left on device
```

## Writing into an image

As you can see singularity is very strict to who can interact with an image and what can be written there.

To write into an image just add `--writable` flag.

```Bash
# Login as a sudo in writable mode
user@machine:~/containerized-workshop$ sudo singularity shell --writable alpine.img
Singularity: Invoking an interactive shell within container...

Singularity alpine.img:~> apk update
Singularity alpine.img:~> apk add vim
Singularity alpine.img:~> exit

user@machine:~/containerized-workshop$ singularity shell alpine.img
Singularity alpine.img:~> vim
Singularity alpine.img:~> exit
```

## Singularity file

We know that it's a bit of a hassle to do everything from terminal. Fortunately, we can automatize our work and create singularity bootstrap file which is equivalent to a Dockerfile.

Create Singularity file (`~/containerized-workshop/Singularityfile`) and copy-paste bellow content into it.

```
# Singularityfile bootstrap file
Bootstrap: docker
From: alpine:3.6

%runscript

exec echo "The runscript is the containers default runtime command!"

%labels
AUTHOR ludd@cbs.dtu.dk

%post

# OS Update & Upgrade
apk update && apk upgrade

# Install packages
apk add \
  git \
  python \
  py-pip

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

```Bash
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

Send the image it via email, copy it on usb stick or upload to cloud -you name it!, just deliver it to person that you want to share it with.
