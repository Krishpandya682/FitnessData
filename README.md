
# FitnessData Microservice

This project is a microservice for integrating Google Fit data into your application. It allows you to retrieve and analyze fitness data such as steps, calories, and active minutes.

## Features

- Fetch step count from Google Fit
- Retrieve calories expended and active minutes data
- Dockerized for easy deployment

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- [Docker](https://www.docker.com/get-started) installed on your machine
- Google Cloud account for setting up OAuth2 credentials

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Krishpandya682/FitnessData.git
    cd FitnessData
    ```

2. **Set up the virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the Google OAuth2 credentials**:

    - Set up OAuth2 credentials in the [Google Cloud Console](https://console.cloud.google.com/).
    - Download the `credentials.json` file and place it in the root directory of this project.

5. **Run the application**:

    ```bash
    python app.py
    ```

## Running with Docker

1. **Build the Docker image**:

    ```bash
    docker build -t fitness-data-service .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -p 5002:5002 fitness-data-service
    ```

## Usage

Once the service is running, you can interact with it via API endpoints. For example, to fetch step count data, send a GET request to:

```http
GET http://localhost:5002/steps
```

You can use tools like [Postman](https://www.postman.com/) or `curl` to test the endpoints.

## Project Structure

```plaintext
.
├── app.py                # Main application file
├── dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── .gitignore            # Files to ignore in Git
└── venv/                 # Virtual environment (not included in Git)
```
