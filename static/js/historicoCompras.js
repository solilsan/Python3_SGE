
var i = 0

function cargarDatos(){

    $.ajax({
      url: '/cargarHistorialCompras',
      type: 'POST',
      async:false,
      success: function(response) {

        var dataset = JSON.parse(response)['datos']

        debugger

        var data = []

        	if (parseInt(dataset[i][4]) == 1) {
        		data.splice(0, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 2) {
        		data.splice(1, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 3) {
        		data.splice(2, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 4) {
        		data.splice(3, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 5) {
        		data.splice(4, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 6) {
        		data.splice(5, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 7) {
        		data.splice(6, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 8) {
        		data.splice(7, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 9) {
        		data.splice(8, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 10) {
        		data.splice(9, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 11) {
        		data.splice(10, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 11) {
        		data.splice(11, 1, parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        var ctxL = document.getElementById("pieChart").getContext('2d');

		var myLineChart = new Chart(ctxL, {
			type: 'line',
			data: {
				labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiempre", "Octubre", "Noviembre", "Diciembre"],
				datasets: [{
					label: "Queso",
					data: data,
					backgroundColor: [
					'rgba(' + (Math.floor(Math.random() * 255) + 1) + ', ' + (Math.floor(Math.random() * 255) + 1) + ', ' + (Math.floor(Math.random() * 255) + 1) + ', .2)',
					],
					borderColor: [
					'rgba(' + (Math.floor(Math.random() * 255) + 1) + ', ' + (Math.floor(Math.random() * 255) + 1) + ', ' + (Math.floor(Math.random() * 255) + 1) + ', .7)',
					],
					borderWidth: 2
				}]
			},
			options: {
				responsive: true
			}
		});

      },
      error: function(error) {

        console.log(error);

      }
    });

  }

cargarDatos()

$('#siguiente').click(function() {

	i += 1

	cargarDatos()

});