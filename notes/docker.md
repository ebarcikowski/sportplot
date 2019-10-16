# Docker notes

I'm not a docker expert, but I see this project using docker to run SQL
so that I don't need to install that and maintain it on my host PC.

Ultimately, I put this into a Dockerfile.

## Notable websites

I found two pretty useful websites. This is basically what I want
to do
https://www.melvinvivas.com/using-docker-data-volume-with-a-mysql-container/

But I plan to use mariadb, from the Docker Hub mariadb documentation
there is this https://hub.docker.com/_/mariadb.

Towards the bottom of this there is a command that essentially does
what I need

```
docker run --name some-mariadb -v /my/own/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mariadb:tag
```

Which is what I based the following on:

## My setup
For my system, something like:

```
docker run --name esportdb -v /srv/storage/mucho/esport/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p3307:3306 -d mariadb
```

where I am keeping my sql data in a storage location on the host at

```
/srv/storage/mucho/esport/mysql
```

Looking at the running containers I get something like:
```
$ docker container ls                           
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
bbdfdc520ea6        mariadb             "docker-entrypoint.s…"   11 minutes ago      Up 11 minutes       0.0.0.0:3307->3306/tcp   esportdb

```

Yay. Now connect with
```
mysql -h 0.0.0.0 -uroot  -P3307 -p
```

And we're in business.
