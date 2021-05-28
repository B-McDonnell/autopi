FROM pios:latest
ARG setupfile=src/dockertools/setup.sh

# set environment variables
ENV DOCKER_HW_ID_PATH /dockertools/hwid

# setup docker tools
RUN mkdir /dockertools
COPY $setupfile /dockertools/setup.sh
COPY src/dockertools/entrypoint.sh /dockertools/entrypoint.sh
RUN chmod +x /dockertools/setup.sh && \
    chmod +x /dockertools/entrypoint.sh

COPY . /autopi
ENTRYPOINT [ "/bin/sh", "-c", "/dockertools/entrypoint.sh" ]
