(function() {
	'use strict';

	// SERVERURL is defined in the environment and written by the php script
	$.post(SERVERURL + '/server/php-code/action.php', 'type=test', data => {
		console.log(data);
	});

})();