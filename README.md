# Vechicle Detection

This project aims to build a website which detects different types of vehicles from the uploaded image. also counts the images and marks the vehicles.

## Setup and Running

- First clone the repo. and move to the folder
    ```bash
    git clone https://github.com/aswanthabam/Vehicle-Detection
    cd Vehicle-Detection
    ```
- Make sure you installed Docker, get installation instructions from [here](https://docs.docker.com/engine/install/) 
- Then use docker compose to run the server, First build 
    ```bash
    docker compose build
    ```
    > NB : This will install the nessessary packages. also it will download the `yolov3` weights, which is 250+ MB size. so the setup will take some time. wait unitil the setup is completed.
- Then run the container
    ```bash
    docker compose up
    ```
- Now open [http://localhost:3000](http://localhost:3000) in your browser.

## Tech stack

- React
- Vite
- Flask
- opencv and yolov3 modal

> For any queries, contact : aswanth.abam@gmail.com
