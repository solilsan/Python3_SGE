
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
      url: '/cargarInventario',
      type: 'POST',
      async:false,
      success: function(response) {

        var dataSet = JSON.parse(response)['datos']

        var table = $('#dt-select').DataTable({
          data: dataSet,
            columns: [
              {title: "id", visible: false},
              {title: "Nombre"},
              {title: "Tipo"},
              {title: "Cantidad"},
              {title: "Precio Compra"},
              {title: "Precio Venta"},
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

  if ($('#cpNombre').val() == "" || $('#cpTipo').val() == "" || $('#cpCantidad').val() == "" || $('#cpPrecioCompra').val() == "" || $('#cpPrecioVenta').val() == "" || parseInt($('#cpCantidad').val()) < 0 || parseFloat($('#cpPrecioCompra').val()) < 0 || parseFloat($('#cpPrecioVenta').val()) < 0){

    valido = false
  }

  return valido

}

$('#crearProducto').click(function() {

  if (validarC()){

      $('#modalCrearProducto').hide();

        $.ajax({
            url: '/crearProducto',
            data: $('#crearProductoForm').serialize(),
            type: 'POST',
            async:false,
            success: function(response) {

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

function validarA(){

  let valido = true

  if ($('#vpNombre').val() == "" || $('#vpTipo').val() == "" || $('#vpCantidad').val() == "" || $('#vpPrecioCompra').val() == "" || $('#vpPrecioVenta').val() == "" || parseInt($('#vpCantidad').val()) < 0 || parseFloat($('#vpPrecioCompra').val()) < 0 || parseFloat($('#vpPrecioVenta').val()) < 0){

    valido = false
  }

  return valido

}

  $('#actualizarProducto').click(function() {

    if (validarA()){

        $('#modalVerProducto').hide();

        $.ajax({
            url: '/actualizarProducto',
            data: $('#actualizarProductoForm').serialize(),
            type: 'POST',
            async:false,
            success: function(response) {

                location.reload();

            },
            error: function(error) {

                console.log(error);

            }
        });

      }
      else {
        return false
      }

    });

function borrar(data){

    $.ajax({
            url: '/borrarInventario',
            data: { idInventario : data },
            type: 'POST',
            async:false,
            success: function(response) {

              location.reload();

            },
            error: function(error) {

                console.log(error);

            }
        });

}

function modificar(data){

  $.ajax({
            url: '/verProducto',
            data: { idInventario : data },
            type: 'POST',
            success: function(response) {

              datos = JSON.parse(response)['datos']

              $('#vpId').val(datos[0]);
              $('#vpNombre').val(datos[1]);
              $('#vpTipo').val(datos[2]);
              $('#vpCantidad').val(parseInt(datos[3]));
              $('#vpPrecioCompra').val(parseFloat(datos[4]));
              $('#vpPrecioVenta').val(parseFloat(datos[5]));

              $('#modalVerProducto').modal('show');

            },
            error: function(error) {

                console.log(error);

            }
        });

}