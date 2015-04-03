$(document).ready(function () {
	if (typeof rank_users != 'undefined') {
		var i, users = '';
		for (i = 0; i < 10; ++i) {
			$('#user-rank-table').append('<tr>'
				+ '<td>' + rank_users[i][0] + '</td>'
				+ '<td><a class="disabled" href="javascript:void(0)" id="voj-account-' + rank_users[i][1] + '">'
				+ rank_users[i][1] + '</a></td>'
				+ '<td>' + rank_users[i][3] + '</td>'
				+ '</tr>');

			if (i > 0) {
				users += ';';
			}
			users += rank_users[i][1];
		}

		$.ajax('/user/get_user_from_voj_account/' + users, {
			dataType: 'json',
			success: function (data) {
				var users = JSON.parse(data);
				console.log(users);
				for (var id = 0; id < users.length; id += 1) {
					var user = users[id];
					console.log(user);
					console.log(user['fields']['voj_account']);
					$('#voj-account-' + user['fields']['voj_account'])
						.attr('href', '/user/' + user['pk'])
						.removeClass('disabled');
				}
			}
		});
	}
});