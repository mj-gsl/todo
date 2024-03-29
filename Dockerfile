# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy wait-for-it.sh script
COPY wait-for-it.sh /app/wait-for-it.sh

# Give execute permissions to the script
RUN chmod +x /app/wait-for-it.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MYSQL_DATABASE_HOST=mysql

# Run app.py when the container launches
CMD ["./wait-for-it.sh", "mysql_container:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
