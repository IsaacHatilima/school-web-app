const notify = document.getElementById('notify')
$('#request_password').submit(function (e)  {
    e.preventDefault();
    document.getElementById("submit").disabled = true;
    notify.style.display = "block";
    $("#heading").html('Processing!');
    $("#msg").html('Please Wait...');
    $("#notify").removeClass("alert-success alert-warning alert-danger").addClass("alert-info");
    let email = $('#email').val();
    var payload = { email: email};
    $.ajax({
        url: auth_forgot_password,
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
                    $("#heading").html('Success!');
                    $("#msg").html(message);
                    $("#notify").removeClass("alert-info alert-warning alert-danger").addClass("alert-success");
                    setTimeout(function () {
                            window.location.href = auth_login;
                    }, 2500);
                    
                }
                else if (status === 400) {
                    $("#heading").html('Warning!');
                    $("#msg").html(message);
                    $("#notify").removeClass("alert-info alert-success alert-danger").addClass("alert-warning");
                    document.getElementById("submit").disabled = false;
                }
            }
        },
        error: function (data) {
            $("#heading").html('Warning!');
            $("#msg").html('Internal Server Error');
            $("#notify").removeClass("alert-info alert-warning alert-success").addClass("alert-danger");
            document.getElementById("submit").disabled = false;
        }
    });

}) 