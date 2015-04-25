function setCodeforcesColor(data) {
	var cfElement = $('#my-codeforces-account');
	if (data.status == 'OK') {
		var rating = data.result[0]['rating'], color;
		if (rating >= 2200) color = 'red';
		else if (rating >= 1900) color = '#FF8C00';
		else if (rating >= 1700) color = '#a0a';
		else if (rating >= 1500) color = 'blue';
		else if (rating >= 1200) color = 'green';
		else color = 'gray';
		cfElement.css('color', color);
	}
}

$(document).ready(function () {
	if ($("#id_dob.form-control").length > 0) {
		$("#id_dob.form-control").datepicker({
			'dateFormat': 'yy-mm-dd',
			'altFormat': 'yy-mm-dd',
			'changeYear': true,
			'changeMonth': true,
			'yearRange': 'c-40:c+10'
		});
	}

	var cfElement = $('#my-codeforces-account');
	if (cfElement.length > 0) {
		var account = cfElement.text();
		$.ajax({
			url: 'http://codeforces.com/api/user.info?handles={account}&jsonp=setCodeforcesColor'.supplant({account: account}),
			jsonp: 'setCodeforcesColor',
			dataType: 'jsonp'
		});
	}
});