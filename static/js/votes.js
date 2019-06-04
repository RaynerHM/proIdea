$(document).ready(function () {

	$("body").on("click", "a.tooltipped", function vote_by_idea(event) {
		let id_idea = $(this).attr('value');
		let type_vote = $(this).attr('type_vote');

		$.ajax({
			type: "POST",
			url: "votes_ajax",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'id_idea': id_idea,
				'type_vote': type_vote,
			},

			success: function (data) {
				$(`#-vote_${id_idea}`).text(data.dont_like);
				$(`#vote_${id_idea}`).text(data.like);

				if (type_vote == 'positive') {
					$(`a[id=-a_${id_idea}]`).removeClass('disabled');
					$(`a[id=a_${id_idea}]`).addClass('disabled');
				}
				else if (type_vote == 'negative') {
					$(`a[id=-a_${id_idea}]`).addClass('disabled');
					$(`a[id=a_${id_idea}]`).removeClass('disabled');
				}
			},
			error: function (data) {
				let content = {
					'html': '<span>Error: ' + data.message + '</span>',
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(content);

			}
		});

	});

	$("#menu_accion input[type=checkbox]").on('change', function idea_validation(){
		let checkBox = this;
		let decition = $(checkBox).attr('id').split('_')[1];
		let id_idea = $(checkBox).attr('id').split('_')[2];
		let status_discarded, status_approved;

		if (this.checked) {
			if (decition == 'approved') {
				$('#check_discarded_' + id_idea)[0].checked = false;
				status_discarded = 'False'
				status_approved = 'True';
			} else {
				$('#check_approved_' + id_idea)[0].checked = false;
				status_approved = 'False'
				status_discarded = 'True';
			}
		}else{
			if (decition == 'approved') {
				$('#check_discarded_' + id_idea)[0].checked = true;
				status_discarded = 'True'
				status_approved = 'False';
			} else {
				$('#check_approved_' + id_idea)[0].checked = true;
				status_approved = 'True';
				status_discarded = 'False';
			}
		}

		$.ajax({
			type: "POST",
			url: "validate_rrhh",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'decition': decition,
				'status_discarded': status_discarded,
				'status_approved': status_approved,
				'id_idea': id_idea,
			},

			success: function (data) {
				if (data.status == 'approved'){
					let content = {
						'html': '<span>' + data.message + '</span>',
						'classes': 'rounded green text-white',
						'displayLength': 10000,
						'outDuration': 5000,
						'inDuration': 2000,
					}
					M.toast(content);
				} else if(data.status == 'discarded'){
					let content = {
						'html': '<span>' + data.message + '</span>',
						'classes': 'rounded red text-white',
						'displayLength': 10000,
						'outDuration': 5000,
						'inDuration': 2000,
					}
					M.toast(content);
				}
			},

			error: function (data) {
				let content = {
					'html': '<span>Error: ' + data.message + '</span>',
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(content);

			}
		});

	});

});
