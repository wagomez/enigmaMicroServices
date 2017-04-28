FROM waltergomezb/gatewayapi-base
MAINTAINER WALTER GOMEZ

RUN apt-get update && \
    apt-get install -qy python-dev
ADD requirements.txt /

# Activate virtual environment and install wheel support
RUN . /appenv/bin/activate && \
    pip3.5 install -r requirements.txt

# PIP environment variables (NOTE: must be set after installing wheel)
ENV NSO_IP=192.168.0.220

# OUTPUT: Test reports are output here
VOLUME /reports

# Add test entrypoint script
COPY scripts/stage.sh /usr/local/bin/stage.sh
RUN chmod +x /usr/local/bin/stage.sh

# Set defaults for entrypoint and command string
ENTRYPOINT ["stage.sh"]
CMD ["python3", "microsvc/msGetDevices.py"]

EXPOSE 5052

# Add application source
COPY src /application
WORKDIR /application
