# Use an official Python runtime as a parent image
FROM python:3.12.1-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port  8000 available to the world outside this container
EXPOSE  8000

# Define environment variables
ARG EMAIL_HOST_PASSWORD
ARG EMAIL_HOST_USER
ARG POSTGRES_URL
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ENV POSTGRES_URL=$POSTGRES_URL

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
