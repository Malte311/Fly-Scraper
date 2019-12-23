<?php

handle_request();

/**
 * Handles incoming HTTP requests.
 */
function handle_request() {
	if (!isset($_POST['type'])) {
		die;
	}

	switch($_POST['type']) {
		case 'onload': // Load site
			$data = load_data();
			echo $data;
			break;
		case 'add': // Create new entry
			try {
				echo add_entry(); // echo true if success, else false
			} catch (Exception $e) {
				echo false;
			}
			break;
	}
}

/**
 * Loads available data.
 * @param int list ID of the list which data should be loaded.
 */
function load_data($list) {

}

/**
 * Adds a new entry to the watchlist.
 * @return bool True if entry was added successfully, else false. 
 */
function add_entry() {
	if (!isset($_POST['from']) || !isset($_POST['to'])
		|| !isset($_POST['depart']) || !isset($_POST['return'])
		|| !isset($_POST['cabin']) || !isset($_POST['travellers'])
	) {
		return false;
	}

	if (!is_string($_POST['from']) || preg_match('/[^a-zA-Z]/', $_POST['from']) || strlen($_POST['from']) > 50
		|| !is_string($_POST['to']) || preg_match('/[^a-zA-Z]/', $_POST['to']) || strlen($_POST['to']) > 50
		|| !is_string($_POST['depart']) || !preg_match('/\d\d\/\d\d\/\d\d\d\d/', $_POST['depart'])
		|| !is_string($_POST['return']) || !preg_match('/\d\d\/\d\d\/\d\d\d\d/', $_POST['return'])
		|| !is_string($_POST['cabin']) || !in_array($_POST['cabin'], array('Economy', 'Premium Economy', 'Business class', 'First class'))
		|| !is_numeric($_POST['travellers']) || preg_match('/[^0-9]/', $_POST['travellers']) || strlen($_POST['travellers']) > 3
	) {
		return false;
	}

	$timestamp = time();
	$data = array(
		'id' => sha1($timestamp),
		'date' => strval($timestamp),
		'from' => $_POST['from'],
		'to' => $_POST['to'],
		'depart' => $_POST['depart'],
		'return' => $_POST['return'],
		'cabin' => $_POST['cabin'],
		'travellers' => $_POST['travellers']
	);

	$file = __DIR__ . '/data/entries.json';
	if (!file_exists($file)) {
		$content = array();
	} else {
		$content = json_decode(file_get_contents($file), true);
	}

	$content[] = $data;
	file_put_contents($file, json_encode($content, JSON_PRETTY_PRINT));

	return true;
}

/**
 * Removes an entry from the watchlist.
 */
function delete_entry() {

}

?>