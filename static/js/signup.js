/**
 * Created by Jonas on 03/06/2017.
 */
$(function() {
    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/signup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});