function readURL(input) {
    if (input.files && input.files[0]) {
	var reader = new FileReader();

	reader.onload = function (e) {
	    $('#image_source').attr('src', e.target.result);
	}

	reader.readAsDataURL(input.files[0]);
    }
}

$("#file_source").change(function(event){
    $('#submit').trigger( "click" );
});

$(document).on('click', '#trigered_button', function(){
  $("#file_source").trigger('click');
});

