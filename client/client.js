(function() {
	'use strict';

	add_datepicker();

	show_info();

	// SERVERURL is defined in the environment and written by the PHP script
	$.post(SERVERURL + '/action.php', 'type=state', data => {
		update_state(JSON.parse(data)); // Adds options for select elements dynamically
	});

	$.post(SERVERURL + '/action.php', 'type=onload', data => {
		show_watchlist(JSON.parse(data)); // Loads all items from the watchlist
	});

})();

/**
 * Adds datepicker to input fields for selecting dates.
 */
function add_datepicker() {
	$('#input-depart').datepicker({
		format: 'yyyy-mm-dd',
		todayHighlight: true,
		autoclose: true
	});

	$('#input-return').datepicker({
		format: 'yyyy-mm-dd',
		todayHighlight: true,
		autoclose: true
	});
}

/**
 * Shows information messages (depending on get paramters).
 */
function show_info() {
	switch (window.location.search) {
		case '?succ_add':
			show_message('Added new entry successfully!', 'green');
			break;
		case '?fail_add':
			show_message('Failed to add new entry due to invalid input!', 'red');
			break;
		case '?succ_del':
			show_message('Deleted entry successfully!', 'green');
			break;
		case '?fail_del':
			show_message('Failed to delete entry!', 'red');
			break;
		case '?succ_listadd':
			show_message('Added new list successfully!', 'green');
			break;
		case '?succ_listren':
			show_message('Renamed list successfully!', 'green');
			break;
		case '?succ_listdel':
			show_message('Deleted list successfully!', 'green');
			break;
		case '?fail_list':
			show_message('Failed to adjust list!', 'red');
			break;
	}
}

/**
 * Displays information messages.
 * @param {string} msg The message to be displayed. 
 * @param {string} color The color of the information message. Possible colors are
 * red, green and blue.
 */
function show_message(msg, color) {
	$('#div-message').removeClass();

	switch (color) {
		case 'blue':
			$('#div-message').addClass('alert alert-info');
			break;
		case 'green':
			$('#div-message').addClass('alert alert-success');
			break;
		case 'red':
			$('#div-message').addClass('alert alert-danger');
			break;
		default:
			$('#div-message').addClass('alert alert-info');
			break;
	}

	$('#div-message').html(msg);
	$('#div-message').show();
}

/**
 * Loads the DOM state.
 * @param {array} data Array of JSON objects containing the DOM state represenation.
 */
function update_state(data) {
	for (list of JSON.parse(data)) {
		let keys = Object.keys(list);
		$('#sel-list1').append(new Option(keys[0], list[keys[0]]));
		$('#sel-list2').append(new Option(keys[0], list[keys[0]]));
	}
}

/**
 * Displays the watchlist.
 * @param {array} data Array of JSON objects for each watchlist entry.
 */
function show_watchlist(data) {
	$('#div-watchlist').html(JSON.parse(data));
}

/**
 * Renames the currently selected list.
 */
function rename_list() {
	$('#sel-listaction').val('rename'); // Set HTTP Post request action type
	let list_name = $("#sel-list2 option:selected").html();
	let input = prompt('Please type in a new name for "' + list_name + '".');
	
	if (input != null) {
		$('#sel-newname').val(input);
		return true;
	}

	return false;
}

/**
 * Adds a new list.
 */
function add_list() {
	$('#sel-listaction').val('add'); // Set HTTP Post request action type
	let input = prompt('Please type in a name for the new list.');

	if (input != null) {
		$('#sel-newname').val(input);
		return true;
	}

	return false;
}

/**
 * Deletes the currently selected list.
 */
function delete_list() {
	$('#sel-listaction').val('delete'); // Set HTTP Post request action type
	let list_name = $("#sel-list2 option:selected").html();
	let input = confirm('Do you really want to delete "' + list_name + '"?');

	if (input == true) {
		return true;
	} else {
		return false;
	}
}