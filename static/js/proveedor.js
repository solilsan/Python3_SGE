
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