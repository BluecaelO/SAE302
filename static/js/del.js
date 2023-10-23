function del_password(value) {
    if (confirm("Are you sure you want to delete this password ?")) {
      $.ajax({
        type: "POST",
        url: "/del_password?pass_name=" + value, // on défini l'url où envoyer les données  pour traitemment (ici suppression)
        success: function(data) {
            $("#password_table").html(data);
        }
      });
    }
  }
// Ici on utilsie de l'ajax pour changer de façon dynamique le contenu d'un div
