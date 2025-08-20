# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user for security (best practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Give the user permissions to the directory
RUN chown -R appuser:appuser /app

# Switch to the new user
USER appuser

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Set the command to run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]