
function cargarDatos(){

    $.ajax({
      url: '/cargarHistorialCompras',
      type: 'POST',
      async:false,
      success: function(response) {

        var dataset = JSON.parse(response)['datos']

        var data = []

        for (var i = 0; i < dataset.length; i++) {
        	debugger
        	if (parseInt(dataset[i][4]) == 1) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 2) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 3) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 4) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 5) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 6) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 7) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 8) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 9) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 10) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 11) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        	if (parseInt(dataset[i][4]) == 11) {
        		data.push(parseInt(dataset[i][1]))
        	}
        	else {
        		data.push(0)
        	}

        }

        debugger

        var ctxL = document.getElementById("pieChart").getContext('2d');

		var myLineChart = new Chart(ctxL, {
			type: 'line',
			data: {
				labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiempre", "Octubre", "Noviembre", "Diciembre"],
				datasets: [{
					label: "My First dataset",
					data: data,
					backgroundColor: [
						'rgba(105, 0, 132, .2)',
					],
					borderColor: [
						'rgba(200, 99, 132, .7)',
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