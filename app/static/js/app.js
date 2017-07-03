$(function() {
    $('#submit').click(function(event) {
        event.preventDefault();
        var form_data = new FormData($('#uploadform')[0]);
	$("#results").empty();
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
	    $("#results_div").show();
	    $("#properties").show();
	    $.each(data['results'], function( key, value ) {
		$("#results").append(value);
	    });
        }).fail(function(data){
            alert('error!');
        });
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
	var reader = new FileReader();

	reader.onload = function (e) {
	    $('#image_source').attr('src', e.target.result);
	}

	reader.readAsDataURL(input.files[0]);
    }
}

$("#file_source").change(function(){
    readURL(this);
    $('#image_source').show();
    $('#submit').trigger( "click" );
});
