(function() {
	'use strict';

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

	// SERVERURL is defined in the environment and written by the php script
	$.post(SERVERURL + '/action.php', 'type=state', data => {
		update_state(JSON.parse(data));
	});

	$.post(SERVERURL + '/action.php', 'type=onload', data => {
		show_watchlist(JSON.parse(data));
	});

})();

/**
 * Loads the DOM state.
 * @param {array} data Array of JSON objects containing the DOM state represenation.
 */
function update_state(data) {
	console.log(data)
	for (list of JSON.parse(data)) {
		let keys = Object.keys(list);
		$('#sel-list1').append('<option>', {value: list[keys[0]], text: keys[0]});
		$('#sel-list2').append('<option>', {value: list[keys[0]], text: keys[0]});
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
 * Hides information messages.
 */
function hide_message() {
	$('#div-message').hide();
}

/**
 * Displays information messages.
 * @param {string} msg The message to be displayed. 
 */
function show_message(msg) {
	$('#div-message').html(msg);
	$('#div-message').show();
}