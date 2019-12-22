<?php

error_reporting(!empty($_ENV['PROD']) && $_ENV['PROD'] == 'prod' ? 0 : E_ALL);

$SERVERURL = !empty($_ENV['SERVERURL']) ? $_ENV['SERVERURL'] : 'http://localhost:8000';

echo str_replace('{$SERVERURL}', $SERVERURL, file_get_contents(__DIR__ . '/client/template.html'));

?>