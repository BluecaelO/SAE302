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
            // Remplacement du contenu de l'élément "table-container" avec les données du tableau
            $("#password_table").html(data);
        }
    });
}

function search_category(value) {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "search?category=" + encodeURIComponent(value),
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "table-container" avec les données du tableau
            $("#password_table").html(data);
        }
    });
}

function search_fav(value) {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "search?fav=" + encodeURIComponent(value),
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "table-container" avec les données du tableau
            $("#").html(data);
        }
    });
}