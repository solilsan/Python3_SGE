
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

$('#botonCrearCompra').click(function() {

  $.ajax({
      url: '/selectInventario',
      type: 'POST',
      async, false,
      success: function(response) {

        var data = JSON.parse(response)['datos']

        debugger

        $("#sProductos").append('<option value='+data[0][0]+' selected>'+data[0][1]+'</option>');

      },
      error: function(error) {
          console.log(error);
      }
  });

  return false

});