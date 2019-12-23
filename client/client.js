(function() {
	'use strict';

	$('#input-depart').datepicker({
		format: 'mm/dd/yyyy',
		todayHighlight: true,
		autoclose: true
	});

	$('#input-return').datepicker({
		format: 'mm/dd/yyyy',
		todayHighlight: true,
		autoclose: true
	});

	// SERVERURL is defined in the environment and written by the php script
	// $.post(SERVERURL + '/action.php', 'type=onload', data => {
	// 	show_message(data);
	// });

})();

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