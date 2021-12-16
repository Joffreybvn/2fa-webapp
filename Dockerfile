FROM python:3.9-slim-buster

# Install the security updates.
RUN apt-get update
RUN apt-get -y upgrade

# Install ubuntu dependencies
RUN apt-get install -y libzbar0

# Remove all cached file. Get a smaller image.
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

EXPOSE 8501

# Copy the application.
COPY . /opt/app
WORKDIR /opt/app

# Install the app librairies.
RUN pip install -r requirements.txt

# Start the app.
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "main.py" ]
