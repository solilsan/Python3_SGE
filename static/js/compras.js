
$(document).ajaxStart(function() { 

    $('#dt-select_wrapper').hide();
    $('#div_carga').show();

});
$(document).ajaxStop(function() { 

    $('#div_carga').hide();
    $('#dt-select_wrapper').show();

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
      async: false,
      success: function(response) {

        $("#sProductos").empty();

        var data = JSON.parse(response)['datos']

        if (data.length > 1){

          $("#sProductos").append('<option value='+data[0][0]+' selected>'+data[0][1]+'</option>');
  
          for (var i = 1; i < data.length; i++) {
            $("#sProductos").append('<option value='+data[i][0]+'>'+data[i][1]+'</option>');
          }

        }
        else {

          $("#sProductos").append('<option value='+data[0][0]+' selected>'+data[0][1]+'</option>');

        }

      },
      error: function(error) {
          console.log(error);
      }
  });

  $.ajax({
      url: '/selectProveedor',
      type: 'POST',
      async: false,
      success: function(response) {

        $("#sProveedor").empty();

        var data = JSON.parse(response)['datos']

        if (data.length > 1) {

          $("#sProveedor").append('<option value='+data[0][0]+' selected>'+data[0][1]+'</option>');
  
          for (var i = 1; i < data.length; i++) {
            $("#sProveedor").append('<option value='+data[i][0]+'>'+data[i][1]+'</option>');
          }

        }
        else {

          $("#sProveedor").append('<option value='+data[0][0]+' selected>'+data[0][1]+'</option>');

        }

      },
      error: function(error) {
          console.log(error);
      }
  });

  $('#modalCrearCompra').modal('show');

  return false

});