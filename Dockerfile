FROM python:3.10-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the requirements file and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files with correct ownership
COPY --chown=user . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 7860

# Start the application
CMD python manage.py migrate && gunicorn blog_project.wsgi:application --bind 0.0.0.0:7860
