document.getElementById("inputPassword").addEventListener('change', function(){
    var pw = this.value;
    if (pw.length < 8) {
        this.classList.add('is-invalid');
    } else {
        this.classList.remove('is-invalid');
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