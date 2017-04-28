FROM waltergomezb/gatewayapi-base
MAINTAINER WALTER GOMEZ

RUN apt-get update && \
    apt-get install -qy python-dev

# Activate virtual environment and install wheel support
RUN . /appenv/bin/activate && \
    pip3.5 install wheel --upgrade


# PIP environment variables (NOTE: must be set after installing wheel)
ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache
ENV NSO_IP=192.168.0.220
# OUTPUT: Build artefacts (Wheels) are output here
VOLUME /wheelhouse

# OUTPUT: Test reports are output here
VOLUME /reports

# Add test entrypoint script
COPY scripts/run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

# Set defaults for entrypoint and command string
ENTRYPOINT ["run.sh"]
CMD ["python3", "microsvc/msAPIsetService.py"]

EXPOSE 5054

# Add application source
COPY src /application
WORKDIR /application
