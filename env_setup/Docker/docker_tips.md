# What is Docker
<details>
    <summary>Click Me</summary>
    
First what is a container? https://www.docker.com/resources/what-container
A unit of software that has the code and all its dependencies on all environments. A Docker container image has the code, runtime, system tools, system libraries and settings all in one place. 
    
Seems like it is almost a virtual environment, with subtle differences. The end result however is to take dependencies, and smoosh them together with code, all inside a container for easy runtime :)
</details>

# Hello world to Docker
<details>
    <summary>Click Me</summary>
    
1. https://docs.docker.com/get-started/#download-and-install-docker
    
    Dockerfile: 
    * We build on top of the `FROM`. 
    * We work in `WORKDIR`
    * We allow access through `ENV`
    * We can copy something and put it into the container?
    * Then we use `RUN` to run stuff on the shell. Npm is a node package manager.
    * Dockerignore files, they denote what files for docker to completely ignore (very similar to gitignore in fact I think they are called the same thing)
    * `CMD` gives a default command for the image to run. ["node", "src/server.js"]

    Getting started website: https://docs.docker.com/get-started/02_our_app/
    Getting started github: https://github.com/docker/getting-started

1. Sample Application: https://docs.docker.com/get-started/02_our_app/
    * We get a base image, we copy the current repo into the container, then we can install extra applications into the container, and finally we run a default command. On our commandline we dimply type `docker build -t getting-started .` which builds the container, tags it getting-started, and tells it where the Dockerfile is located.
    * We then run 
    * `docker run -dp 3000:3000 getting-started`, to attach port 3000 to port 3000 and we know what container to run. The d runs this as detatched in the background.

1. Update the application: https://docs.docker.com/get-started/03_updating_app/
    * Just gotta update the script on the local machine, run a new docker build, and then run it. We get an error because the old container is still running, lets fix that.
    * To see all the dockers running, do `docker ps`, the first column is the container ID. Just plug that into `docker stop <container ID>` and voila. We can see all existing dockers with `docker ps -a`. Can rm all of them with 
    * `docker rm $(docker ps -a -f status=exited -q)`
    * We also need to remove it with `docker rm <container ID>` but IDK what that is about.

</details>

# Tips and tricks
<details open>
    <summary>Click Me</summary>
   
1. Farshad suggested that when building a single cell environment, try to get a docker working for `Seurat` first because it has a crazy list of dependancies.
    
1. Cleanliness
    1. We can view our stopped docker images with `docker ps -a`
    1. `docker system prune` I'm sure there are better more safe ways to do this: https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

1. Storing work
    1. Volumes
We can use volumes! Volumens are like this magical way to have a container output be stored on the local machine. <br><br> We initialize a volume like so: `docker run -it -v data:/magicfolder f965d580bf6f` where data is the local name of the volume, and `/magicfolder` is the name of where I want my data to go, and the hash is the image id. <br><br>Now this data folder on the local machine is magical and exists somewhere, but I haven't been able to find it!!!

1. Bind Mounts
This is similar to to volumnes, but lets us use data on the host's machine as input.<br><br>We can mount a host directory with a similar command: `docker run -v "$PWD/data":/data -w /data 81ed47240d23 ls ..`. **NOTE**: After the image id, you can enter basically any command that you want run on the container and it will run. For example I can do script.py sample.txt because it was added to the contianer path!<br><br>**NOTE** that for the host path, it needs the full path which we can access with `$PWD`<br><br>We can give a long command to the docker run by using `bash -c "long command ; separated by ; semicolons"` Thank you https://dzone.com/articles/pass-multiple-commands-on-docker-run    
    
1. View what commands were used to make a Dockerfile with 
`docker image history --no-trunc <image code> > image_history`
1. Run an interactive shell inside a containter with `docker run -it <imagename> sh`
1. When a container is already running you can enter it with `docker exec -it <containerID> bash`
    
</details>
