
$(document).ajaxStart(function() { 

    $('#dt-select_wrapper').hide();
    $('#div_carga').show();

});
$(document).ajaxStop(function() { 

    $('#div_carga').hide();
    $('#dt-select_wrapper').show();

});

var table

function cargarDatos(){

    $.ajax({
      url: '/cargarProveedores',
      type: 'POST',
      success: function(response) { 

        var dataSet = JSON.parse(response)['datos']

        table = $('#dt-select').DataTable({
          data: dataSet,
            columns: [
              {title: "id", visible: false},
              {title: "Nombre"},
              {title: "Dirección"},
              {title: "Teléfono"},
              {title: "Controles"}
            ],
            dom: 'Bfrtip',
            select: false
        });

      },
      error: function(error) {

        console.log(error);

      }
    });

  } 

cargarDatos()

function validarC(){

  let valido = true

  if ($('#nombreProveedor').val() == ""){

    valido = false
  }

  return valido

}

$('#crearProveedor').click(function() {

  if (validarC()){

      $('#modalCrearProveedor').modal('hide');

        $.ajax({
            url: '/newProveedor',
            data: $('#crearProveedorForm').serialize(),
            type: 'POST',
            async:false,
            success: function(response) {

              table.destroy();
              cargarDatos()

            },
            error: function(error) {

                console.log(error);

            }
        });

        return false

      }
      else {

        return false

      }

    });

function borrar(data){

    $.ajax({
            url: '/borrarProveedor',
            data: { idProveedor : data },
            type: 'POST',
            async:false,
            success: function(response) {

              table.destroy();
              cargarDatos()

            },
            error: function(error) {

                console.log(error);

            }
        });

    return false

}