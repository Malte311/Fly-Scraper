<?php

$DATA_FILE = __DIR__ . '/data/entries.json';

handle_request();

/**
 * Handles incoming HTTP requests.
 */
function handle_request() {
	if (!isset($_POST['type'])) {
		die;
	}

	$list = isset($_POST['list']) && is_numeric($_POST['list']) && strlen($_POST['list']) < 5 ? $_POST['list'] : 0;
	$param = '';
	switch($_POST['type']) {
		case 'onload': // Load watchlist data
			echo load_data($list);
			return;
		case 'add': // Create new entry
			try {
				$param = add_entry($list) ? 'succ_add' : 'fail_add';
			} catch (Exception $e) {
				$param = 'fail_add';
			}
			break;
		case 'delete':
			break;
		case 'list':
			$a = isset($_POST['action']) && is_string($_POST['action']) && strlen($_POST['action']) < 20 ? $_POST['action'] : '';
			switch ($a) {
				case 'rename':
					$param = 'succ_listren';
					break;
				case 'add':
					$param = 'succ_listadd';
					break;
				case 'delete':
					$param = 'succ_listdel';
					break;
				default:
					$param = 'fail_list';
					break;
			}
			break;
		case 'state': // Load DOM state
			echo load_lists();
			return;
	}

	header('Location: ' . (!empty($_ENV['SERVERURL']) ? $_ENV['SERVERURL'] : 'http://localhost:8000') . '/?' . $param);
	http_response_code(303);
}

/**
 * Loads all available lists.
 */
function load_lists() {
	$file = __DIR__ . '/data/lists.json';
	if (!file_exists($file)) {
		file_put_contents($file, json_encode(array(array('Default watchlist' => 0)), JSON_PRETTY_PRINT));
	}
	
	return json_encode(file_get_contents($file));
}

/**
 * Loads available data.
 * @param int list ID of the list which data should be loaded.
 * @return array Array of JSON objects for each entry.
 */
function load_data($list) {
	global $DATA_FILE;

	if (!file_exists($DATA_FILE)) {
		return json_encode(array());
	} else {
		return json_encode(file_get_contents($DATA_FILE));
	}
}

/**
 * Adds a new entry to the watchlist.
 * @param int list ID of the list to which data should be added.
 * @return bool True if entry was added successfully, else false.
 */
function add_entry($list) {
	global $DATA_FILE;

	if (!isset($_POST['from']) || !isset($_POST['to'])
		|| !isset($_POST['depart']) || !isset($_POST['return'])
		|| !isset($_POST['cabin']) || !isset($_POST['travellers'])
	) {
		return false;
	}

	if (!is_string($_POST['from']) || preg_match('/[^a-zA-Z]/', $_POST['from']) || strlen($_POST['from']) > 50
		|| !is_string($_POST['to']) || preg_match('/[^a-zA-Z]/', $_POST['to']) || strlen($_POST['to']) > 50
		|| !is_string($_POST['depart']) || !preg_match('/\d\d\d\d-\d\d-\d\d/', $_POST['depart'])
		|| !is_string($_POST['return']) || !preg_match('/\d\d\d\d-\d\d-\d\d/', $_POST['return'])
		|| !is_string($_POST['cabin']) || !in_array($_POST['cabin'], array('Economy', 'Premium Economy', 'Business class', 'First class'))
		|| !is_numeric($_POST['travellers']) || preg_match('/[^0-9]/', $_POST['travellers']) || strlen($_POST['travellers']) > 3
	) {
		return false;
	}

	$timestamp = time();
	$data = array(
		'id' => sha1($timestamp),
		'date' => strval($timestamp),
		'list' => $list,
		'from' => $_POST['from'],
		'to' => $_POST['to'],
		'depart' => $_POST['depart'],
		'return' => $_POST['return'],
		'cabin' => $_POST['cabin'],
		'travellers' => $_POST['travellers']
	);

	if (!file_exists($DATA_FILE)) {
		$content = array();
	} else {
		$content = json_decode(file_get_contents($DATA_FILE), true);
	}

	$content[] = $data;
	file_put_contents($DATA_FILE, json_encode($content, JSON_PRETTY_PRINT));

	return true;
}

/**
 * Removes an entry from the watchlist.
 */
function delete_entry() {

}

?>