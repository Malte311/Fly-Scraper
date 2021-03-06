FROM kimbtechnologies/php_nginx:php-7.4.2

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" > /etc/apk/repositories \
	&& echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories \
	&& apk update \
	&& apk add python3 \
	&& apk add chromium=77.0.3865.120-r0 \
	&& apk add chromium-chromedriver \
	&& pip3 install selenium 

RUN mkdir /py-code/ \
	&& mkdir /py-code/drivers/ \
	&& chown -R www-data:www-data /py-code/ \
	&& mkdir /php-code/data/ \
	&& chown -R www-data:www-data /php-code/data/ \
	&& mkdir /php-code/client/ \
	&& chown -R www-data:www-data /php-code/client/ \
	&& echo $' \n\
	# url rewriting error pages \n\
	error_page 404 /index.php?uri=err404; \n\
	error_page 403 /index.php?uri=err403; \n\
	# protect private directories \n\
	location ~ ^/(data){ \n\
		deny all; \n\
		return 403; \n\
	} \n\
	' > /etc/nginx/more-server-conf.conf

RUN wget -q "https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /py-code/drivers/ \
    && rm /tmp/chromedriver.zip

RUN ln -s /usr/bin/chromium-browser \
    && chmod 777 /usr/bin/chromium-browser

COPY --chown=www-data:www-data ./py-code/ /py-code/
COPY --chown=www-data:www-data ./index.php /php-code/index.php
COPY --chown=www-data:www-data ./action.php /php-code/action.php
COPY --chown=www-data:www-data ./data/ /php-code/data/
COPY --chown=www-data:www-data ./client/ /php-code/client/

COPY ./setup.sh /startup-before.sh

ENV PROD=prod
