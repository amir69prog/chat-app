function disply_form(){
    var btn_submit = document.getElementById("submit-btn");
    var btn_edit = document.getElementById("edit-btn");
    btn_submit.classList.remove('d-none');
    btn_edit.classList.add("d-none")
    undisplay()
}

function undisplay(){
    var username = document.getElementById("id_username").disabled = false;
    var email = document.getElementById("id_email").disabled = false;
    var first_name = document.getElementById("id_first_name").disabled = false;
    var last_name = document.getElementById("id_last_name").disabled = false;
    var biography = document.getElementById("id_biography").disabled = false;
    var profile_picture = document.getElementById("id_profile_picture").disabled = false;
    var nickname = document.getElementById("id_nickname").disabled = false;
}