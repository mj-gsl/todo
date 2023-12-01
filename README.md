
---

# FastAPI ToDo App with MySQL Docker Setup

This repository provides a Docker setup for running a FastAPI ToDo App with a MySQL database. The Docker Compose configuration includes both the FastAPI application and a MySQL database, ensuring a seamless and portable deployment.

## Prerequisites

Before you begin, ensure that you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/fastapi-todo-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd fastapi-todo-app
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

   This command will download the necessary Docker images, build the FastAPI and MySQL containers, and start the application.

4. Access the FastAPI ToDo App:

   Once the containers are up and running, you can access the FastAPI ToDo App at [http://localhost:8000/](http://localhost:8000/).

## Usage

- The FastAPI application is running on port 8000.
- The MySQL database is running on port 3307.

### FastAPI Endpoints

- **Home Page:** [http://localhost:8000/](http://localhost:8000/)
- **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Swagger UI:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### MySQL Connection

- **Host:** `localhost`
- **Port:** `3307`
- **Database:** `todo_app`
- **User:** `todouser`
- **Password:** `Passw0rd`

## Stopping the Application

To stop the Docker containers, press `Ctrl + C` in the terminal where the `docker-compose up` command is running.

## Notes

- The MySQL data is persisted in the `./mysql-data` directory.
- Make sure to wait for both containers to fully start before accessing the application.

## Issues and Contributions

If you encounter any issues or have suggestions for improvements, feel free to [open an issue](https://github.com/your-username/fastapi-todo-app/issues) or create a pull request.

Happy coding!

---

This README provides users with clear instructions on how to set up and use your FastAPI ToDo App with MySQL Docker configuration. Feel free to enhance it based on your project's specific details.