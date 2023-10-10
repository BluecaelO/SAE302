
// exemple de resuête ajax de SAE203

function delpwd(value) {
    if (confirm("Voulez-vous vraiment supprimer ce mot de passe?")) {
      $.ajax({
        type: "POST",
        url: "" + value,
        success: function(data) {
            $("#table-container").html(data);
        }
      });
    }
  }
  
  
function updatepwd(valeur) {
  if (confirm("Voulez-vous vraiment mettre à jour le mot de passe ?")) {
      $.ajax({
        type: "POST",
        url: "" + valeur,
        success: function(data) {
            $("#table-container").html(data);
        }
      });
  }
}

let target="customers";

function direction(value) {
  target=value;  
}
  
  
function search(value) {
      // Envoi de la requête AJAX au serveur
  $.ajax({
    type: "GET",
    url: "/table/" + target + ".php?table=search&Svalue=" + value,
    success: function(data) {
              // Traitement des données récupérées
              // Remplacement du contenu de l'élément "table-container" avec les données du tableau
      $("#table-container").html(data);
    }
  });
}