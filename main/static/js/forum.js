$(document).ready(function () {
	$('.post-delete').click(function () {
		var clickedElement = $(this);
		$('#post-delete-confirm-dialog').dialog({
			buttons: {
				'OK': function () {
					window.location = '/forum/{post_id}/post_delete'.supplant({
						'post_id': clickedElement.attr('post-id')
					});
				},
				'Cancel': function() {
					$(this).dialog('close');
				}
			}
		});
	});
});