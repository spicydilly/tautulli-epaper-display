FROM arm32v7/python:3.11-slim-buster

# Setting the working directory in the Docker container
WORKDIR /app/

# Copy the needed resources
COPY resources/ resources/

# Get dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    fonts-dejavu-core \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements file
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# cleanup
RUN apt-get remove -y gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copying the Python scripts
COPY src/ src/

# Adding the cron job
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab \
    && /usr/bin/crontab /etc/cron.d/crontab

# Set Timezone
ENV TZ="Europe/London"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
