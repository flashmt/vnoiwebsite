$(document).ready(function() {
    if (typeof rank_users != 'undefined') {
        var i;
        for (i = 0; i < 10; ++i) {
            $('#user-rank-table').append('<tr>'
                + '<td>' + rank_users[i][0] + '</td>'
                + '<td>' + rank_users[i][1] + '</td>'
                + '<td>' + rank_users[i][3] + '</td>'
                + '</tr>');
        }
    }
});