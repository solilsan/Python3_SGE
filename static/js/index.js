
$( document ).ready(function() {
    
    $('#botonLogin').click(function() {
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {

                if (response == "1") {

                    $("#lCorrecto").addClass("d-none");
                    location.href='inicio.html'
                }
                else {

                    $("#lCorrecto").removeClass("d-none");
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#logout').click(function() {
        $.ajax({
            url: '/logout',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {

                if (response == "1") {

                    location.href='index.html'
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });

});