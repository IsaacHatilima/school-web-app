//Check Email
function checkEmail()
{ 
    let email = $("#email").val();
    filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    const email_error = document.getElementById('email_error')
    if (filter.test(email)) {
        $("#email").removeClass("border-danger danger").addClass("border-primary success");
        var payload = { email: email };
        $.ajax({
            url: check_email,
            data: payload,
            type: "POST",
            dataType: "json",
            headers: {
                content_type: 'application/json',
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data) {
                    var status = data.status
                    if (status === 200) {
                        email_error.style.display = "none";
                        $("#email").removeClass("border-danger danger").addClass("border-primary success");
                    }
                    else {
                        email_error.style.display = "block";
                        $("#email").removeClass("border-primary success").addClass("border-danger danger");
                    }
                }
            },
            error: function () {
                console.log('Error')
            }
        }); 
    }
    else
    {
        $("#email").removeClass("border-primary success").addClass("border-danger danger");
    }
}

//Check Username
function checkUsername()
{ 
    let username = $("#username").val();
    const username_error = document.getElementById('username_error')
    if (username.length >= 5) {
        $("#username").removeClass("border-danger danger").addClass("border-primary success");
        var payload = { username: username };
        $.ajax({
            url: check_username,
            data: payload,
            type: "POST",
            dataType: "json",
            headers: {
                content_type: 'application/json',
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data) {
                    var status = data.status
                    if (status === 200) {
                        username_error.style.display = "none";
                        $("#username").removeClass("border-danger danger").addClass("border-primary success");
                    }
                    else {
                        username_error.style.display = "block";
                        $("#username").removeClass("border-primary success").addClass("border-danger danger");
                    }
                }
            },
            error: function () {
                console.log('Error')
            }
        }); 
    }
    else
    {
        $("#username").removeClass("border-primary success").addClass("border-danger danger");
    }
}