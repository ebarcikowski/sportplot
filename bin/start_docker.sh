#!/bin/bash
# Since I'm somewhat new to docker, I'll just do this with a script
# for now. Hopefully, I'll turn this into a docker file at some point.
#
# Getting started with this guide:
# https://www.melvinvivas.com/using-docker-data-volume-with-a-mysql-container/
#
# From the mariadb notes on Docker Hub:
# https://hub.docker.com/_/mariadb
function create_volume() {
    docker create -v /srv/storage/mucho/esport/sql --name esportdata mariadb
}

function start() {
    docker run --name esportdb --volumes-from esportdata -e MYSQL_ROOT_PASSWORD=password -p 3307:3306 mariadb
}
