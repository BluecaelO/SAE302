function delete_password() {
    // Envoi de la requête AJAX au serveur
    $.ajax({
        type: "POST",
        url: "search?fav=1",
        success: function(data) {
            // Traitement des données récupérées
            // Remplacement du contenu de l'élément "table-container" avec les données du tableau
            $("#password_table").html(data);
        }
    });
}