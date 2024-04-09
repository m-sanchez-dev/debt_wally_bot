# Use the official Python 3.12.2 image as base
FROM python:3.12.2

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# docker run -p 5000:5000 -e BOT_TOKEN=<your_bot_token> -e URL=<your_webhook_url> my-telegram-bot
