
function cargarDatos(){

    $.ajax({
      url: '/cargarHistorialCompras',
      type: 'POST',
      async:false,
      success: function(response) {

        var dataSet = JSON.parse(response)['datos']

        debugger

        var ctxL = document.getElementById("pieChart").getContext('2d');

		var myLineChart = new Chart(ctxL, {
			type: 'line',
			data: {
				labels: ["January", "February", "March", "April", "May", "June", "July"],
				datasets: [{
					label: "My First dataset",
					data: [65, 59, 80, 81, 56, 55, 40],
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