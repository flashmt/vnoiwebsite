// This file should be loaded for all pages after JS libraries and before all other scripts.

// HELPER METHODS

// String interpolation method
// Usage:
// "I'm {age} years old!".supplant({ age: 29 });
// "The {a} says {n}, {n}, {n}!".supplant({ a: 'cow', n: 'moo' });
// "The {0} says {1}, {1}, {1}!".supplant(['cow', 'moo'])
String.prototype.supplant = function (o) {
    return this.replace(/{([^{}]*)}/g,
        function (a, b) {
            var r = o[b];
            return typeof r === 'string' || typeof r === 'number' ? r : a;
        }
    );
};
// END OF HELPER METHODS



// CONSTANT DECLARATIONS
VOTING_URL = "/forum/vote/{post_id}/?type={vote_type}";
// END OF CONSTANT DECLARATIONS



// METHODS THAT SHOULD BE COMMON TO ALL PAGES
$(document).ready(function () {
	$('[data-toggle="offcanvas"]').click(function () {
		$('.row-offcanvas').toggleClass('active')
	});

	// Handling clicking on up-vote / down-vote. Since these elements are shown in home page + forum topic retrieve
	// page, I'm putting these methods here.

	function changeVote(type) {
		return function () {
			var clickedElement = $(this);
			var postId = clickedElement.attr('post-id');
			var totalVoteElement = $("#total-vote-{post_id}".supplant({post_id: postId}));
			var currentVote = parseInt(totalVoteElement.text(), 10);

			console.log("Current vote = " + currentVote);
			console.log("type = " + type);

			$.ajax({
				url: VOTING_URL.supplant({
					post_id: postId,
					vote_type: type
				}),
				success: function (data) {
					console.log(data);
					$.jGrowl(data['message'], {position: 'bottom-right'});
					if (data['success'] == 1) {
						if (type == 'u') {
							totalVoteElement.text(currentVote + 1);
						}
						else {
							totalVoteElement.text(currentVote - 1);
						}
					}
				},
				dataType: 'json'
			});
		}
	}
	$('.post-upvote').click(changeVote('u'));
	$('.post-downvote').click(changeVote('d'));
	$('.home-post-upvote').click(changeVote('u'));
	$('.home-post-downvote').click(changeVote('d'));
});
