# Download Docker image of sphinxneeds hosted in BDC JFrog Artifactory Docker Registry
# The following statement must reference a specific tag, not just latest
FROM artifactory.boschdevcloud.com/zugspitze-series-docker-local/ad-radar-sensor-docker-doc-as-code/sphinxneeds-toolkit:2.0.0

# If you get proxy errors, make sure Docker is configured following the 
# instructions here: https://inside-docupedia.bosch.com/confluence/x/V5nDXQ

USER root

# To prevent interactive shells
ENV DEBIAN_FRONTEND=noninteractive

# Upgrade as needed
RUN apt-get update && apt-get upgrade -y

# Install basic utils needed inside devcontainer
RUN \
  apt-get install -qqy curl zip && \
  apt-get install -qqy bash && \
  apt-get install -qqy apt-transport-https

# Set the locale
RUN apt-get update && \
  apt-get install -qqy locales locales-all

ENV LC_ALL de_DE.UTF-8
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE.UTF-8

# Set timezone inside Docker container
ENV TZ=Europe/Berlin

RUN echo $TZ > /etc/timezone && \
  apt-get update && apt-get install -qqy tzdata && \
  rm /etc/localtime && \
  dpkg-reconfigure -f noninteractive tzdata

WORKDIR /documentation
USER dockeruser
