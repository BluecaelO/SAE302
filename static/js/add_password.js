function generate_password() {
    var length = document.getElementById("length").value;
    var upercases = document.getElementById("add_upercases");
    var lowercases = document.getElementById("add_lowercases");
    var numbers = document.getElementById("add_numbers");
    var specials = document.getElementById("add_specials");

    var charset = "";

    if (upercases.checked) {
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    }
    if (lowercases.checked) {
        charset += "abcdefghijklmnopqrstuvwxyz";
    }
    if (numbers.checked) {
        charset += "0123456789";
    }
    if (specials.checked) {
        charset += "!@#$%^&*()";
    }

    var retVal = "";
    for (var i = 0, n = charset.length; i < length; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
    }
    console.log(retVal);
    document.getElementById("password").value = retVal;
}



function copyPassword() {
    var copyText = document.getElementById("password");
    copyText.select();
    document.execCommand("copy");
  }

