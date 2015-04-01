$(document).ready(function () {
	if ($("#id_dob.form-control").length > 0) {
		$("#id_dob.form-control").datepicker({
			'dateFormat': 'yy-mm-dd',
			'altFormat': 'yy-mm-dd'
		});
	}
});