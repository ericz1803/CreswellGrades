document.getElementById("inputUsername").addEventListener('change', function(){
    var uname = this.value;
    console.log(this.classList);
    $.ajax({
        url: '/ajax/username-taken/'.concat(uname),
        type: "GET",
        success: function(response){
            if (response['taken']) {
                document.getElementById("inputUsername").classList.add('is-invalid');
            } else {
                document.getElementById("inputUsername").classList.remove('is-invalid');
            }
        }
    });
});

document.getElementById("inputPassword").addEventListener('change', function(){
    var pw = this.value;
    if (pw.length < 8) {
        this.classList.add('is-invalid');
    } else {
        this.classList.remove('is-invalid');
    }
});

document.getElementById("inputFirstname").addEventListener('change', function(){
    var val = this.value;
    if (val.length > 0) {
        this.classList.remove('is-invalid');
    } else {
        this.classList.add('is-invalid');
    }
});

document.getElementById("inputLastname").addEventListener('change', function(){
    var val = this.value;
    if (val.length > 0) {
        this.classList.remove('is-invalid');
    } else {
        this.classList.add('is-invalid');
    }
});

document.getElementById("inputConfirmPassword").addEventListener('change', function(){
    var pw = document.getElementById("inputPassword").value
    var pw_confirm = this.value;
    if (pw != pw_confirm) {
        this.classList.add('is-invalid');
    } else {
        this.classList.remove('is-invalid');
    }
});

$('form').on('keyup change paste', 'input, select, textarea', function(){
    if (document.getElementsByClassName('is-invalid').length === 0) {
        document.getElementById("submitButton").disabled = false;
    } else {
        document.getElementById("submitButton").disabled = true;
    }
});