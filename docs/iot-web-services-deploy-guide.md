# IoT Web Services Deploy Guide

This guide aims to provide an instruction guide about how to manually deploy web-based applications as docker containers onto GCP.

## Prerequisite

### 1. docker Setup

1. You need to ensure you have a working docker env locally by following this official site: https://docs.docker.com/get-docker/. If docker env is running properly, you should be able to run the following commands in CLI without errors:

   ```
   docker --version
   docker ps
   docker images
   ```

### 2. GCP Setup

1. You need to be able to access to the company GCP cloud console under the project `sit-22t2-redback-infra-612f89e` using your own Deakin student email.

2. Follow this official guide to install `gcloud` CLI to your local env: https://cloud.google.com/sdk/docs/install. Once it's installed, run `gcloud -v` to verify it works fine.

3. Run `gcloud auth login` in CLI. This will open up a new browser window, and you can login to GCP using your Deakin email.

## Containerize Your Web Application

1. Under the root directory of your web application, you need to create a `Dockerfile` file and provide detailed procedures to be run while Containerizing your app into a docker image. Follow this reference for more details about `Dockerfile`: https://docs.docker.com/engine/reference/builder/

   - An example of a React FE application `Dockerfile` can be found here: https://github.com/redbackoperations/iot/blob/main/sensors-cms-frontend/Dockerfile
   - An example of a Nodejs BE application `Dockerfile` can be found here: https://github.com/redbackoperations/iot/blob/main/sensors-backend/Dockerfile

2. Once the `Dockerfile` is ready, run `docker build -t YOUR-DOCKER-IMAGE-NAME-HERE .` under your app's root folder to build a docker image for the app.

3. After the new docker image is built, you can start up a new container using the image like: `docker run -d -it -p 3000:3000 YOUR-DOCKER-IMAGE-NAME-HERE` (change the port numbers to any proper values you want)

4. Run `docker ps -a` to verify your container has been running now.

5. You can verify your web application now by accessing to the corresponding `localhost` address. For example:

   - If your app is a FE web app, and you've configured the container port like `3001:3001` in step 3, then you should have your app be reachable at: http://localhost:3001 in browser.
   - If your app is a BE web app, and you've configured the container port like `3000:3000` in step 3, then you should have your app server be reachable at: http://localhost:3000/ in browser (assuming your BE app has configured to accept a base path `/` request).
   - If your web service is not a HTTP-based app, you can also run `docker logs CONTAINER_ID_FROM_DOCKER_PS_CMD` to check its running logs and see if it's running properly

## Access into Your Docker Container Env

1. Run `docker exec -it CONTAINER_ID_HERE /bin/sh` to access into your docker container's shell env.

## Tag and Push Docker Images to GCP

1. Once you've verified that your docker container is working fine locally, you can tag your container and push it to the remote GCP Container Registry by the followings:

   ```
     # to get your local image tag name
     docker images

     # Tag your local image as a pushable docker image to GCP, the new tag name pattern needs to be "GCP_REGION_NAME/GCP_PROJECT_NAME/REMOTE_IMAGE_NAME_HERE:IMAGE_VERSION", for instance:
     docker tag LOCAL_IMAGE_TAG_NAME asia.gcr.io/sit-22t2-redback-infra-612f89e/REMOTE_IMAGE_NAME_HERE:v1.0

     # double check your newly tagged image is in the list
     docker images

     # push your tagged image to GCP now, for instance:
     docker push asia.gcr.io/sit-22t2-redback-infra-612f89e/REMOTE_IMAGE_NAME_HERE:v1.0
   ```

2. The docker image of your application is now ready for deploying to GCP cloud.

3. You can go to GCP cloud console -> Container Registry page to check if your pushed docker image there.

4. In GCP Container Registry, copy the `docker pull` command for the docker image you've just pushed.

## Deploy

1. In GCP, you can deploy your docker container by either "Cloud Run" or "Compute Engine Virtual Machine". please follow the official guide to setup the corresponding GCP cloud service to host your docker containers:

- https://cloud.google.com/run/docs/deploying
- https://cloud.google.com/compute/docs/create-linux-vm-instance

2. In GCP VM instance, for instance, you can manually `docker pull` your docker image onto the VM. Once you have pulled the docker image on the VM, you can run `docker run -d -it -p 127.0.0.1:3000:3000 YOUR_DOCKER_IMAGE_NAME` or `docker run -d -it -p 0.0.0.0:3000:3000 YOUR_DOCKER_IMAGE_NAME` (change the port numbers to what you want) to start up your container on the VM. After the container is up running, you can now access to your web application remotely at `http://PUBLIC_IP_ASSIGNED_TO_THE_GCP_VM:3000`.

3. If your application needs to be guarded with request proxy, HTTPS connection, basic auth, you may also config and setup a separate `Nginx` service on your VM, then link your docker container `IP_ADDRESS:PORT_NUMBER` into the Nginx service.
