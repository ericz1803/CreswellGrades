var email = false;
var password = false;
var password_valid = false;
var password_match = false;

document.getElementById("email").addEventListener('change', function() {
    if (this.value.length > 0) {
        email = true;
    } else {
        email = false;
    }
});

document.getElementById("inputPassword").addEventListener('change', function(){
    var pw = this.value;
    if (document.getElementById("inputConfirmPassword").value.length == 0 && pw.length == 0) {
        password = false;
    } else {
        password = true;
    }

    if (pw.length < 8 && pw.length != 0) {
        this.classList.add('is-invalid');
        password_valid = false;
    } else {
        this.classList.remove('is-invalid');
        password_valid = true;
    }
});

document.getElementById("inputConfirmPassword").addEventListener('change', function(){
    var pw = document.getElementById("inputPassword").value
    var pw_confirm = this.value;
    if (pw_confirm.length && pw.length == 0) {
        password = false;
    } else {
        password = true;
    }

    if (pw != pw_confirm) {
        this.classList.add('is-invalid');
        password_match = false;
    } else {
        this.classList.remove('is-invalid');
        password_match = true;
    }
});

$('form').on('keyup change paste', 'input, select, textarea', function(){
    if (password_valid && password_match || email && !password) {
        document.getElementById("submitButton").disabled = false;
    } else {
        document.getElementById("submitButton").disabled = true;
    }
});