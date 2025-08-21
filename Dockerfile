# Use a robust Python runtime as a parent image
FROM python:3.10-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies (as root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create a non-root user for security (best practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Give the user permissions to the directory
RUN chown -R appuser:appuser /app

# Switch to the new user before running the application
USER appuser

# Set the command to run the app using Waitress
CMD ["waitress-serve", "--listen=0.0.0.0:8080", "app:app"]
EXPOSE 8080