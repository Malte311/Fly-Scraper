var flights = {};
var flight_info = {};

$(function() {
	'use strict';

	add_datepicker();

	add_listener();

	show_info();

	load_page();
});

/**
 * Loads the page.
 */
async function load_page() {
	// SERVERURL is defined in the environment and written by the PHP script
	let stateData = await Promise.resolve(
		$.post(SERVERURL + '/action.php', $.param({'type': 'state'}))
	);
	update_state(JSON.parse(stateData)); // Adds options for select elements dynamically

	let data = await Promise.resolve(
		$.post(SERVERURL + '/action.php', $.param({'type': 'onload'}))
	);
	flights = typeof data === 'string' ? JSON.parse(data) : data;
	show_watchlist(flights); // Loads all items from the watchlist

	let info = await Promise.resolve(
		$.post(SERVERURL + '/action.php', $.param({'type': 'data'}))
	);
	flight_info = typeof info === 'string' ? JSON.parse(info) : info;
	show_flight_information(flight_info);
}

/**
 * Adds datepicker to input fields for selecting dates.
 * @param {string} startDate The start date of the second datepicker
 * (the second date can only be after the first one).
 */
function add_datepicker(startDate = null) {
	$('#input-depart').datepicker({
		format: 'yyyy-mm-dd',
		todayHighlight: true,
		autoclose: true
	});

	$('#input-depart').change(() => {
		$('#input-return').datepicker('remove');
		add_datepicker($('#input-depart').val());
	});

	let date = new Date(startDate);
	date.setDate(date.getDate() + 1);
	$('#input-return').datepicker({
		format: 'yyyy-mm-dd',
		todayHighlight: true,
		autoclose: true,
		startDate: date
	});
}

/**
 * Adds listener to some elements.
 */
function add_listener() {
	$('#sel-list2').change(event => {
		show_watchlist(flights);
		show_flight_information(flight_info);
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
	for (list of data) {
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
	const header = ['from', 'to', 'depart', 'return', 'cabin', 'travellers', 'threshold'];
	
	let hrow = '';
	for (col of header) {
		let n = header.indexOf(col);
		hrow += '<th scope="col" num="' + n + '">' + col.charAt(0).toUpperCase() + col.slice(1) + '</th>';
	}
	hrow += '<th scope="col" num="' + (header.length + 1) + '">Delete</th>';

	let rows = '';
	for (entry of data) {
		if (parseInt(entry.list) === parseInt($('#sel-list2').val())) {
			rows += '<tr>';
			for (col of header) {
				rows += '<td>' + entry[col] + '</td>';
			}
			rows += '<td><a href="#" onclick="delete_entry(\'' + entry.id + '\')">&#10060;</a></td></tr>';
		}
	}

	let thead = '<table id="tab" class="table table-striped"><thead class="thead-dark"><tr>' + hrow + '</tr></thead>';
	let tbody = '<tbody>' + rows + '</tbody></table>';
	$('#div-watchlist').html(thead + tbody);

	if (rows == '') { // No entries yet
		$('#div-watchlist').append('So far, there are no entries.');
	}

	$(`#tab thead tr th`).each(function() { // function for this binding
		$(this).click(() => {
			sortTable(parseInt($(this).attr('num')), 'tab');
		});
	});
}

/**
 * Displays the flight information for each flight.
 * 
 * @param {array} flight_info Array of JSON objects for each flight.
 */
function show_flight_information(flight_info) {
	$('#div-infos').html('');
	for (flight of flight_info) {
		let entry = flights.find(value => value['id'] === flight['id']);
		// Only display information for flights in the currently selected list
		if (parseInt(entry['list']) === parseInt($('#sel-list2').val())) {
			let url_key = Object.keys(flight).find(key => flight[key][0].url !== undefined);
			if (url_key === undefined) continue;
			
			let url = flight[url_key][0].url;
			let text = `${entry.from} &ndash; ${entry.to}`;
			let title = `<h5><a class="text-dark" href="${url}" target="_blank">${text}</a></h5>`;
			let time = `Depart: ${entry.depart}, Return: ${entry.return}`;
			let passenger = `${entry.cabin}, ${entry.travellers} travellers`;
			let canvas = `<canvas id="${entry.id}" width="500" height="300">`;
			
			let html = '<div>' + title + time + '<br>' + passenger + '<br>' + canvas + '</div>';
			$('#div-infos').append(html);
			
			show_chart(flight);
		}
	}
}

/**
 * Displays the chart for given flights.
 * 
 * @param {object} flight_data JSON object containing the data to be visualized.
 */
function show_chart(flight_data) {
	let colors = [
		'rgba(80, 189, 255, 1)', 'rgba(0, 204, 0, 1)', 'rgba(255, 99, 132, 1)',
		'rgba(255, 165, 0, 1)', 'rgba(255, 215, 0, 1)', 'rgba(106, 90, 205, 1)',
		'rgba(0, 100, 0, 1)', 'rgba(30, 144, 255, 1)', 'rgba(138, 43, 226, 1)',
		'rgba(238, 130, 238, 1)', 'rgba(255, 0, 0, 1)', 'rgba(0, 0, 255, 1)'
	];

	let datasets = {};
	for (let data of Object.keys(flight_data)) {
		if (/^\d\d\d\d-\d\d-\d\d$/.test(data)) {
			// Index 0 has only the 'url' attribute, so we start at 1
			for (let i = 1; i < flight_data[data].length; i++) {
				let f = flight_data[data][i];
				let key = `${f.airlines.join(', ')}${f.time}${f.duration}${f.stay}${f.stops}`;

				if (key in datasets) {
					datasets[key]['data'].push(parseInt(f.price));
				} else {
					datasets[key] = {
						backgroundColor: colors[(i - 1) % colors.length],
						borderColor: colors[(i - 1) % colors.length],
						data: [parseInt(f.price)],
						label: `${f.airlines.join(', ')}`,
						fill: false
					};
				}
			}
		}
	}
	
	new Chart(flight_data['id'], {
		type: 'line',
		data: {
			labels: Object.keys(flight_data).filter(val => /^\d\d\d\d-\d\d-\d\d$/.test(val)),
			datasets: Object.values(datasets)
		}
	});
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

	if (input == true) { // return input
		return true;
	} else {
		return false;
	}
}

/**
 * Deletes an entry.
 * @param {number} The ID of the entry which should be deleted.
 */
function delete_entry(id) {
	let input = confirm('Do you really want to delete this entry?');

	if (input == true) {
		let obj = {
			"type" : "delete",
			"id": id
		};
		$.post(SERVERURL + '/action.php', obj, data => {
			flights = JSON.parse(data);
			show_watchlist(flights);
		});
	}
}

/**
 * Sorts a table by a specified column.
 * Source: https://www.w3schools.com/howto/howto_js_sort_table.asp
 * 
 * @param {number} n The index of the column to sort by.
 * @param {string} tableId The id of the table we want to sort.
 */
function sortTable(n, tableId) {
	var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	table = document.getElementById(tableId);
	switching = true;
	// Set the sorting direction to ascending:
	dir = "asc";
	/* Make a loop that will continue until
	no switching has been done: */
	while (switching) {
		// Start by saying: no switching is done:
		switching = false;
		rows = table.rows;
		/* Loop through all table rows (except the
		first, which contains table headers): */
		for (i = 1; i < (rows.length - 1); i++) {
			// Start by saying there should be no switching:
			shouldSwitch = false;
			/* Get the two elements you want to compare,
			one from current row and one from the next: */
			x = rows[i].getElementsByTagName("TD")[n];
			y = rows[i + 1].getElementsByTagName("TD")[n];
			/* Check if the two rows should switch place,
			based on the direction, asc or desc: */
			if (dir == "asc") {
				if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
					// If so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			} else if (dir == "desc") {
				if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
					// If so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			}
		}
		if (shouldSwitch) {
			/* If a switch has been marked, make the switch
			and mark that a switch has been done: */
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
			// Each time a switch is done, increase this count by 1:
			switchcount++;
		} else {
			/* If no switching has been done AND the direction is "asc",
			set the direction to "desc" and run the while loop again. */
			if (switchcount == 0 && dir == "asc") {
				dir = "desc";
				switching = true;
			}
		}
	}
}