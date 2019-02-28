$("#inputUsername").change(function(){
    var uname = $(this).val();
    $.ajax({
        url: '/ajax/username-taken/'.concat(uname),
        type: "GET",
        success: function(response){
            if (response['taken']) {
                document.getElementById("usernameTaken").style.display = 'block';
            } else {
                document.getElementById("usernameTaken").style.display = 'none';
            }
        }
    });
});

$("#inputPassword").change(function(){
    var pw = $(this).val();
    if (pw.length < 8) {
        document.getElementById("weakPassword").style.display = 'block';
    } else {
        document.getElementById("weakPassword").style.display = 'none';
    }
});

$("#inputConfirmPassword").change(function(){
    var pw = document.getElementById("inputPassword").value
    var pw_confirm = $(this).val();
    if (pw != pw_confirm) {
        document.getElementById("passwordsDontMatch").style.display = 'block';
    } else {
        document.getElementById("passwordsDontMatch").style.display = 'none';
    }
});
