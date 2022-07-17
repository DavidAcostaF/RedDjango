
function abrir_modal_creacion(url) {
	$('#creacion').load(url, function () {
		$(this).modal('show');
	});
}

function cerrar_modal_creacion(){
	$('#creacion').modal('hide');
}