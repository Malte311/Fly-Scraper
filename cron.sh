#!/bin/sh

docker exec --user www-data fly-scraper sh -c "cd /py-code/ && python3 ./run_scraper.py 2"