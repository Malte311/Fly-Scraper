# Fly-Scraper

> Work in progress... (currently, the program is not doing anything useful!)
>
> Also remember that you should not make this service publicly available on your server (because input fields are not protected)!

## Installation (via Docker)

1. Download this repository:

```bash

git clone git@github.com:Malte311/Fly-Scraper.git

```

2. Adjust the `docker-compose.yml` file. Specify the correct server url and port.

```yaml

version: "2"

services:
  web:
    image: malte311/fly-scraper:latest
    container_name: fly-scraper
    ports:
      - "127.0.0.1:8080:80"
    volumes:
      - ./data/:/php-code/data/
    restart: always
    environment:
      - SERVERURL=https://example.com/fly-scraper

```

3. Get the newest Docker image and start a Docker container (inside of the project folder):

```bash

docker-compose pull
docker-compose up -d

```

4. Install a cronjob to run the scraper periodically.

```bash

chmod +x cron.sh
crontab -e -u root

```

A cronjob every 45 minutes could look like this:

```bash

*/45 * * * * /bin/sh /var/docker-compose/fly-scraper/cron.sh

```

Note that the scraper has a session limit of 2 connections per session in order to avoid
too many requests at the same time. This limit can be changed by adjusting the parameter
given to `run_scraper.py` in the file `cron.sh`.
