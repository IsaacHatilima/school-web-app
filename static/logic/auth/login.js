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
    let next = $('#next').val();
    let remember_me = $('#remember_me:checked').val();
    var payload = { email: email, password: password, remember_me:remember_me, next:next };
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
                var destination = data.destination
                if (status === 200) {
                    $("#heading").html('AuthenticatedISAAC!');
                    $("#msg").html('Redirecting, Please Wait...');
                    $("#notify").removeClass("alert-info alert-warning alert-danger").addClass("alert-success");
                    setTimeout(function () {
                            window.location.href = destination;
                    }, 2500); 
                    
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
    