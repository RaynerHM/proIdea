$(document).ready(function() {

	$.ajax({
		type: "GET",
		url: "charge_category_ajax",
		data: {},

		success: function (data) {
			$('input.autocomplete').autocomplete({
				data: data.categorie,
				limit: 4,
				onAutocomplete: function (val) { 
					$('#category_hide').val(data.unique_name_category[val]);
					console.log(data.unique_name_category[val])

				},
			});
		},
		error: function (data) {
			var content = {
				'html': '<span>No se pudieron cargar las categorias.</span>',
				'classes': 'rounded red text-white',
				'displayLength': 10000,
				'outDuration': 5000,
				'inDuration': 2000,
			}
			M.toast(content);
		}
	});
	
});