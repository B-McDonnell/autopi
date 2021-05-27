FROM pios:latest
ARG setupfile=docker_setup.sh

COPY . /autopi

ENV DOCKER_HW_ID_PATH /hwid
COPY $setupfile /setup.sh
RUN chmod +x /setup.sh

ENTRYPOINT [ "/setup.sh" ]
