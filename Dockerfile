FROM kimbtechnologies/php_nginx:latest

RUN apk add --update --no-cache python3 \
	&& pip3 install requests bs4 \
	&& mkdir /py-code/ \
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

COPY --chown=www-data:www-data ./py-code/ /py-code/
COPY --chown=www-data:www-data ./index.php /php-code/index.php
COPY --chown=www-data:www-data ./action.php /php-code/action.php
COPY --chown=www-data:www-data ./data/ /php-code/data/
COPY --chown=www-data:www-data ./client/ /php-code/client/

ENV PROD=prod