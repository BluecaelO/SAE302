function fill_infos(value) {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "fill_infos?pass_name=" + value,
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "table-container" avec les données du tableau
            $("#password_infos").html(data);
        }
    });
}


function PassShow() {
    const passwordToggle = document.querySelector('.js-password-toggle')
    
    passwordToggle.addEventListener('change', function() {
        const password = document.querySelector('.js-password'),
        passwordLabel = document.querySelector('.js-password-label')
    
        if (password.type === 'password') {
        password.type = 'text'
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye-slash"></i>'
        } else {
        password.type = 'password'
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye"></i>'
        }
    
        password.focus()
    })
}

  
function copy(value) {
    var copyText = document.getElementById(value);
    copyText.select();
    document.execCommand("copy");
  }


function copyPassword() {

    const pass = document.getElementById("password")

    pass.type = 'text'

    var copyText = document.getElementById("password");
    copyText.select();
    document.execCommand("copy");

    pass.type = 'password'

}



