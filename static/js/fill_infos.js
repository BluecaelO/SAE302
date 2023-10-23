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


function togglePassword() {
    const passwordToggle = document.querySelector('.js-password-toggle');
    const password = document.querySelector('.js-password');
    const passwordLabel = document.querySelector('.js-password-label');

    if (password.type === 'password') {
        password.type = 'text';
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
    } else {
        password.type = 'password';
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }

    password.focus();
}

// permet de copier l'input de notre choix en fonction de son id
function copy(value) {
    var copyText = document.getElementById(value);
    copyText.select();
    document.execCommand("copy");
}
// les mots de passe ne pouvant pas être copié s'il son caché on les affiche, on les copie puis a les re cache
function copyPassword() {
    const pass = document.getElementById("password");
    pass.type = 'text';

    var copyText = document.getElementById("password");
    copyText.select();
    document.execCommand("copy");

    pass.type = 'password';
}



