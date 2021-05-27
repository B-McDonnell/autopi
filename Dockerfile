FROM pios:latest
ARG setupfile=src/dockertools/setup.sh

# set environment variables
ENV DOCKER_HW_ID_PATH /dockertools/hwid

# setup docker tools
RUN mkdir /dockertools
COPY $setupfile /dockertools/setup.sh
COPY entrypoint /dockertools/entrypoint.sh
RUN chmod +x /dockertools/setup.sh && \
    chmox +x /dockertools/entrypoint.sh

ENTRYPOINT [ "/dockertools/entrypoint.sh" ]
