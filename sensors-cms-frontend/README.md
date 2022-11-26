# IoT CMS Frontend

This is a frontend application of IoT CMS that displaying bikes, devices, and sensors DB stored data in a visualised format like line charts, pie charts or table lists. The app is also used to create/update bikes and devices data as a CMS.

The `/dashboard` page is able to fetch the latest sensors data from DB automatically without a page refresh when there're multiple sensors data report messages sent to MQTT broker. The `/device-data` page is able to search for multiple sensors data using different filters.

## Tech Stacks being Used

- This app is implemented by the latest **React** library (18.2.0).

- Material UI component library (**MUI**) is also used to present better UI and UX.

- All source codes are written by **Typescript** to support for static type checks.

- **Docker** is used to containerise this app as an image, which is then pulled and run on a GCP Compute Engine VM instance as a standalone docker container process.

## Prerequisite

1. Please ensure `Nodejs`(>= v16.0.0) and `npm`(>=7.0.0) have been installed.

2. Ensure you have a MQTT broker url with credentials ready.

3. Ensure you have **IoT Backend** server running locally (without this step, this FE app can be still initiated, yet it just won't show up any data as the backend server is not connected).

4. Ensure port `3001` is available for use locally.

5. Copy `.env.example` to a new `.env` file, and modify the ENV variables to reflect your MQTT broker and backend server configs if needed.

6. To build a new version of docker image, you will also need to install `Docker` locally.

## How to Install and Run Locally

1. Run `npm install` to install all needed packages.

2. Run `npm start` to initiate the front app.

3. You can now open up a browser and go to `http://localhost:3001/` to visit the app.

## How to Create a New Docker Image and Push to GCP Container Registry

1. You need to refer to the official GCP docker docs to authenticate your GCP account locally with Docker first.

2. Under the root folder directory, run `docker build -t cms-fe .` to create a new docker image build.

3. Assign the new build with a new docker tag version like: `docker tag cms-fe {YOUR_GCP_REGION_URL_HERE}/{YOUR_GCP_PROJECT_ID_HERE}/cms-fe:v0.1`.

4. Push the docker image to GCP with `{YOUR_GCP_REGION_URL_HERE}/{YOUR_GCP_PROJECT_ID_HERE}/cms-fe:v0.1`.

5. Now you can pull the newly pushed docker image on the GCP VM instance, stop the old docker container, and start a new container with this new image build. The production IoT FE app is running the latest version build now.

## Extra Notes

- The CMS FE app is now hosted on a GCP Compute Engine VM instance.
- The app can now be visited at `http://34.129.10.237` with proper Basic Auth creds.
- It's fetching sensors data from a backend API server at `http://34.129.10.237:3000`.
