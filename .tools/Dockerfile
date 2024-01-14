# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# List the contents of the working directory
RUN ls -la

# Set the entrypoint command to start the generate.py script
CMD ["python", "src/generate.py"]
