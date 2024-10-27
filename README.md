# Carpooling app

Just a PoC (Proof Of Concept) Car Pooling system implementation. 

# How to Run the Application

This project sets up a Python application inside a Docker container.

## Prerequisites

Make sure you have Docker installed on your machine. You can follow the [Docker installation guide](https://docs.docker.com/get-docker/).

## Steps to Build and Run

### 1. Build the Docker Image

Open a terminal in your project directory and run the following command to build the Docker image:

```bash
docker build -t carpooling-app .
```
## Project Structure

The project contains the following files:

- `main.py`: The main application file (ensure this file exists or adjust the `Dockerfile` accordingly).
- `requirements.txt`: A file listing all Python dependencies required by the application.

## Getting Started

Follow these steps to build and run the application inside a Docker container.

### Step 1: Build the Docker Image

To build the Docker image, run the following command from the project directory:

```bash
docker build -t carpooling-app .
```
This command will create a Docker image named `carpooling-app` using the Dockerfile in the current directory.

### Step 2: Run the Docker Container 

Once the image is built, you can run the application using this command:


```bash
docker run -p 8080:8080 carpooling-app
```
This command maps port `8080` from the container to port `8080` on your local machine, making the application accessible via `http://localhost:8080`.

### Step 3: Access the Application 



### Notes 
 
- Ensure all required Python packages are listed in `requirements.txt`.
 
- If you're using a FastAPI app and prefer to use `uvicorn` instead of `python main.py`, uncomment the `CMD` line in the `Dockerfile` and comment out the `ENTRYPOINT` line.




