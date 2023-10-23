function generate_password() {
    // on  récuprer les ID des différent boutons de la page qui font changer les paramètres de la fonction de génération de mot de passe. On récupére aussi longeur du mot de passe en fonction de valeur de l'input sur la page
    var length = document.getElementById("length").value;
    var upercases = document.getElementById("add_upercases");
    var lowercases = document.getElementById("add_lowercases");
    var numbers = document.getElementById("add_numbers");
    var specials = document.getElementById("add_specials");

    var charset = "";

    // On va ensuite définir la variable charset en fonction des paramètres que l'on a coché pour définir l'ensemble que l'on utilise pour générer les mots de passe
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
    
    // Génération du mot de passe en bouclant sur la longueur souhaitée.
    var retVal = "";
    
    for (var i = 0, n = charset.length; i < length; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
        // Sélection aléatoire d'un caractère dans la chaîne "charset" et ajout à "retVal".
    }
    console.log(retVal);
    document.getElementById("password").value = retVal;
}



function copyPassword() {
    // cette fonction permet de copier les mots de passe que l'on génère
    var copyText = document.getElementById("password");
    copyText.select();
    document.execCommand("copy");
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    const passwordToggle = document.querySelector('.js-password-toggle');
  
    passwordToggle.addEventListener('change', function() {
      const password = document.querySelector('.js-password');
      const passwordLabel = document.querySelector('.js-password-label');
    
        // elle permet aussi de pouvoir afficher le mot de passe en lettres ou en points lorsque l'on clique sur l'icône d'oeil
        // on utilise aussi cette fonction pour changer l'icône d'œil l'on affiche les mots de passe 
      if (password.type === 'password') {
        password.type = 'text';
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
      } else {
        password.type = 'password';
        passwordLabel.innerHTML = '<i class="fa-solid fa-eye"></i>';
      }
  
      password.focus();
    });
  });
  
