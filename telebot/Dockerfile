# Use the Python3.8 image
FROM python:3.8
# Set the working directory to /app

RUN mkdir /code
WORKDIR /code

# Copy the current directory contents into the container at /app 
# ADD . /app
COPY ./requirements.txt .
# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
# CMD ["python3", "/app/main_telebot.py"]