let target="customers";

function direction(value) {
    target=value;  
  }


  function search(value) {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "search?value=" + encodeURIComponent(value),
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "password_table" avec les données du tableau
            $("#password_table").html(data);
        }
    });
}

// On fait la même chose que pour le search mais en donnant une valeur "fav=1" pour les mots de passe en favoris car dans le 
function search_fav() {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "search?fav=1",
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "password_table" avec les données du tableau
            $("#password_table").html(data);
        }
    });
}
