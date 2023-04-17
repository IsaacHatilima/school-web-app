const notify = document.getElementById('notify')

$('#login').submit(function (e)  {
    e.preventDefault();
    document.getElementById("loginBTN").disabled = true;
    notify.style.display = "block";
    $("#heading").html('Authenticating!');
    $("#msg").html('Please Wait...');
    $("#notify").removeClass("alert-success alert-warning alert-danger").addClass("alert-info");
    let email = $('#email').val();
    let password = $('#password').val();
    let remember_me = $('#remember_me:checked').val();
    var payload = { email: email, password: password, remember_me:remember_me };
    $.ajax({
        url: auth_login,
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
                var message = data.msg
                if (status === 200) {
                    window.location.href = auth_2fa;
                }
                else if (status === 403) {
                    $("#heading").html('Warning!');
                    $("#msg").html(message);
                    $("#notify").removeClass("alert-info alert-success alert-danger").addClass("alert-warning");
                    document.getElementById("loginBTN").disabled = false;
                }
            }
        },
        error: function (data) {
            $("#heading").html('Warning!');
            $("#msg").html('Internal Server Error');
            $("#notify").removeClass("alert-info alert-warning alert-success").addClass("alert-danger");
            document.getElementById("loginBTN").disabled = false;
        }
    });

}) 

$('#final_login').submit(function (e)  {
    e.preventDefault();
    document.getElementById("proceed").disabled = true;
    notify.style.display = "block";
    $("#heading").html('Processing!');
    $("#msg").html('Please Wait...');
    $("#notify").removeClass("alert-success alert-warning alert-danger").addClass("alert-info");
    let auth_code = $('#auth_code').val();
    let remember_me = $('#remember_me').val();
    var payload = { auth_code: auth_code, remember_me:remember_me };
    $.ajax({
        url: auth_2fa,
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
                var message = data.msg
                var role = data.role
                if (status === 200) {
                    $("#heading").html('Authenticated!');
                    $("#msg").html('Redirecting, Please Wait...');
                    $("#notify").removeClass("alert-info alert-warning alert-danger").addClass("alert-success");
                    if (role === "System Admin") {
                        setTimeout(function () {
                            window.location.href = admin_home;
                        }, 2500);
                    }
                }
                else if (status === 403) {
                    $("#heading").html('Warning!');
                    $("#msg").html(message);
                    $("#notify").removeClass("alert-info alert-success alert-danger").addClass("alert-warning");
                    document.getElementById("proceed").disabled = false;
                }
            }
        },
        error: function (data) {
            $("#heading").html('Warning!');
            $("#msg").html('Internal Server Error');
            $("#notify").removeClass("alert-info alert-warning alert-success").addClass("alert-danger");
            document.getElementById("proceed").disabled = false;
        }
    });

}) 
    