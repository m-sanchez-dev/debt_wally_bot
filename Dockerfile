# Use the official Python 3.12.2 image as base
FROM python:3.12.2-slim

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies from requirements.txt
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["sh", "-c", "BOT_TOKEN=$BOT_TOKEN URL=$URL /venv/bin/gunicorn --bind 0.0.0.0:5000 --workers $(($(nproc --all) * 2 + 1)) app.app:app"]
