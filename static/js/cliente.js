
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
      url: '/cargarClientees',
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

function validarN(){

  let valido = true

  if ($('#nombreCliente').val() == ""){

    valido = false
  }

  return valido

}

$('#crearCliente').click(function() {

  if (validarN()){

      $('#modalCrearCliente').modal('hide');

        $.ajax({
            url: '/newCliente',
            data: $('#crearClienteForm').serialize(),
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
            url: '/borrarCliente',
            data: { idCliente : data },
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

function modificar(data){

  $.ajax({
            url: '/verCliente',
            data: { idCliente : data },
            type: 'POST',
            success: function(response) {

              datos = JSON.parse(response)['datos']

              $('#idCliente').val(datos[0]);
              $('#nCliente').val(datos[1]);
              $('#cCliente').val(datos[2]);
              $('#tCliente').val(parseInt(datos[3]));

              $('#modalVerCliente').modal('show');

            },
            error: function(error) {

                console.log(error);

            }
        });

}

function validarG(){

  let valido = true

  if ($('#nCliente').val() == ""){

    valido = false
  }

  return valido

}

$('#actualizarCliente').click(function() {

    if (validarG()){

        $('#modalVerCliente').modal('hide');

        $.ajax({
            url: '/actualizarCliente',
            data: $('#actualizarClienteForm').serialize(),
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