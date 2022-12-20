FROM maven:3.8.6-jdk-11 as maven

WORKDIR /usr/src/app
COPY ./src /usr/src/app/src
COPY ./pom.xml /usr/src/app/pom.xml
COPY ./wait-for-it.sh /usr/src/app/wait-for-it.sh
RUN ["ls", "-l", "/usr/src/app/"]
# compile with maven
RUN mvn compile
# Install tree
RUN apt-get update && apt-get install -y tree

RUN ["tree", "/usr/src/app/"]
