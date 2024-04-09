# Use the official Python image as base
FROM python:3.12.2

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies with Poetry
RUN /root/.poetry/bin/poetry install --no-root

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["/root/.poetry/bin/poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# docker run -p 5000:5000 -e BOT_TOKEN=<your_bot_token> -e URL=<your_webhook_url> my-telegram-bot
