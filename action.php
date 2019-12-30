<?php

$DATA_FILE = __DIR__ . '/data/entries.json';

handle_request();

/**
 * Handles incoming HTTP requests.
 */
function handle_request() {
	global $DATA_FILE;

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
			$param = delete_entry($_POST['id']) ? 'succ_del' : 'fail_del';
			echo json_encode(file_get_contents($DATA_FILE));
			return;
		case 'list':
			$a = isset($_POST['action']) && is_string($_POST['action']) && strlen($_POST['action']) < 20 ? $_POST['action'] : '';
			switch ($a) {
				case 'rename':
					$param = rename_list($list, $_POST['newname']) ? 'succ_listren' : 'fail_list';
					break;
				case 'add':
					$param = add_list($_POST['newname']) ? 'succ_listadd' : 'fail_list';
					break;
				case 'delete':
					$param = delete_list($list) ? 'succ_listdel' : 'fail_list';
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
 * Renames a given list.
 * @param int $list The ID of the list which should be renamed.
 * @param string $newname The new name for the list.
 */
function rename_list($list, $newname) {
	if (!is_string($newname) || preg_match('/[^a-zA-Z0-9 ]/', $newname) || strlen($newname) > 50) {
		return false;
	}

	$file = __DIR__ . '/data/lists.json';
	$data = json_decode(file_get_contents($file));
	$new_data = array();
	foreach ($data as $json) {
		foreach ($json as $key => $val) {
			if (strval($val) === strval($list)) {
				$new_data[] = array($newname => $val);
			} else {
				$new_data[] = array($key => $val);
			}
		}
	}

	file_put_contents($file, json_encode($new_data, JSON_PRETTY_PRINT));

	return true;
}

/**
 * Adds a new list.
 * @param string $name The name of the list which should be added.
 */
function add_list($name) {
	if (!is_string($name) || preg_match('/[^a-zA-Z0-9 ]/', $name) || strlen($name) > 50) {
		return false;
	}

	$file = __DIR__ . '/data/lists.json';
	$data = json_decode(file_get_contents($file));
	$last_num = -1;
	foreach ($data as $json) {
		foreach ($json as $key => $val) {
			if (intval($val) > $last_num) {
				$last_num = intval($val);
			}
		}
	}
	$data[] = array($name => $last_num + 1);

	file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));

	return true;
}

/**
 * Deletes a given list.
 * @param int $list The ID of the list which should be deleted.
 */
function delete_list($list) {
	$file = __DIR__ . '/data/lists.json';
	$data = json_decode(file_get_contents($file));
	$new_data = array();
	foreach ($data as $json) {
		foreach ($json as $key => $val) {
			if (strval($val) !== strval($list)) {
				$new_data[] = array($key => $val);
			}
		}
	}

	file_put_contents($file, json_encode($new_data, JSON_PRETTY_PRINT));

	return true;
}

/**
 * Loads available data.
 * @param int $list ID of the list which data should be loaded.
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
 * @param int $list ID of the list to which data should be added.
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
 * @param string $id The ID of the entry which should be deleted.
 */
function delete_entry($id) {
	global $DATA_FILE;

	if (!isset($id) || !is_string($id) || strlen($id) > 50) {
		return false;
	}

	if (!file_exists($DATA_FILE)) {
		return false;
	} else {
		$data = json_decode(file_get_contents($DATA_FILE), true);
		$new_data = array();
		foreach ($data as $entry) {
			if (strval($entry['id']) !== strval($id)) {
				$new_data[] = $entry;
			}
		}
		file_put_contents($DATA_FILE, json_encode($new_data, JSON_PRETTY_PRINT));

		return true;
	}
}

?>