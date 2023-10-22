function del_password(value) {
    if (confirm("Are you sure you want to delete this password ?")) {
      $.ajax({
        type: "POST",
        url: "/del_password?pass_name=" + value,
        success: function(data) {
            $("#password_table").html(data);
        }
      });
    }
  }
