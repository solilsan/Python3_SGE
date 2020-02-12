
$(document).ajaxStart(function() { 

    $('#div_carga').show();

});
$(document).ajaxStop(function() { 

    $('#div_carga').hide();

});


function cargarDatos(){

    $.ajax({
      url: '/cargarCompras',
      type: 'POST',
      success: function(response) { 

        var dataSet = JSON.parse(response)['datos']

        var table = $('#dt-select').DataTable({
          data: dataSet,
            columns: [
              {title: "id", visible: false},
              {title: "Producto"},
              {title: "Proveedor"},
              {title: "Cantidad"},
              {title: "Precio"},
              {title: "Total"},
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