# Use an official Python runtime as the base image
FROM python:3.9 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Copy the cron job file into the cron.d directory
COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Apply the cron job
RUN crontab /etc/cron.d/cronjob

# Expose the port on which the Django app will run
EXPOSE 8000

# Start cron and the Django development server
CMD cron && python manage.py runserver 0.0.0.0:8000 && tail -f /var/log/cron.log