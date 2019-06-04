$(document).ready(function () {

	$('.tooltipped').tooltip({
		enterDelay: 300,
		outDuration: 100,
	});

	$('.dropdown-trigger').dropdown();

	$('.modal').modal();

	$('textarea#description').characterCounter();

	$('#btn_cancel').click(function (event) {
		event.preventDefault()
		$('#modal1').modal('close');
	});


	function recharge() {
		let quantity = $('#inp_quantity').val();

		$.ajax({
			url: 'auto_charge_ideas_ajax',
			type: 'GET',
			data: {
				params: window.location.search,
			},
			success: function (data) {
				$.each(data, function (index, field) {
					$(`#vote_${field['pk']}`).text(field['fields'].quantity_positive_votes);
					$(`#-vote_${field['pk']}`).text(field['fields'].quantity_negative_votes);
				});

				if (quantity < data.length) {
					create_element_li(data);
					$('#inp_quantity').val(data.length);
				};
			},
			error: function (data) {
				console.log('Error al cargar los datos.');
			}
		});
	};

	if (window.location.pathname != "/validate_rrhh") {
		time = setInterval(recharge, 10000);
	};

	function datetime_format(date_django) {

		let time_format = '';
		let date_format = 0;
		let date_complete = 0;

		const DIAS = ['', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'];
		const MESES = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

		let date = date_django.split('T')[0].split('-').reverse();
		let time = date_django.split('T')[1].split('.')[0].split(':');
		date_format = (`${date[0]} de ${MESES[parseInt(date[1])]} de ${date[2]}`);


		if (time[0] < 2) {
			time_format = (` a la ${time[0]}:${time[1]}`);
		}
		else {
			time_format = (` a las ${time[0]}:${time[1]}`);
		}
		date_complete = (date_format + time_format);

		return date_complete;
	};

	function create_element_li(data){
		$('#list_ideas').prepend(
		`<li>
			<div class="card center">
				<div class="card-content">
					<ul>
						<li class="left">
							<span class="card-title">${data[0]['fields'].category}</span>
						</li>
					</ul>
					<p>${data[0]['fields'].description}</p>
				</div>
				<div id="footer" class="card-action row">

					<div id="photo" class="col s6 m6">
						<ul id="datos">
							<li>
								<i class="fas fa-user-circle fa-2x"></i>
							</li>
							<li>
								<p class="author">
									${data[0]['fields'].anonimus ? 'Anónimo' : data[0]['fields'].author }
								</p>
								<p>${datetime_format(data[0]['fields'].publication_date)}</p>
							</li>
						</ul>
					</div>

					<div id="accion" class="col s6 m6">
						<ul>
							<li>
								<a id="-a_${data[0]['pk']}" name="negative" class="${data[0]['fields'].anonimus ? 'Anónimo' : data[0]['fields'].author} btn a_round tooltipped" value="${data[0]['pk']}" type_vote="negative" data-tooltip="No me gusta">
									<i class="far fa-thumbs-down"></i>
								</a>
								<p id="-vote_${data[0]['pk']}">${data[0]['fields'].quantity_negative_votes}</p>
							</li>
							<li>
								<a id="a_${data[0]['pk']}" name="positive" class="btn a_round tooltipped" value="${data[0]['pk']}" type_vote="positive" data-tooltip="Me gusta">
									<i class="far fa-thumbs-up"></i>
								</a>
								<p id="vote_${data[0]['pk']}">${data[0]['fields'].quantity_positive_votes}</p>
							</li>
						</ul>
					</div>

				</div>
			</div>
		</li>`);
	};

	var url = $('#rigobellto').attr('src');
	$('#button_floating')
		.mouseover(function(){
			$('#rigobellto').attr('src', url);
			$('#rigobellto').show();
		})
		.mouseout(function(){
			$('#rigobellto').hide();
			$('#rigobellto').attr('src', '');
		});

});
