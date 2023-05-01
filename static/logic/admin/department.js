$('#make_department').submit(function (e) {
    e.preventDefault();
    // Disable Submit Button
    document.getElementById("makeBTN").disabled = true;
    // Switch button icon to loading Icon
    $("#BTNIcon").removeClass("fa-save").addClass("fa-spinner fa-pulse fa-fw");
    // Get input value
    let department = $('#department').val();
    // Make payload
    var payload = { department: department };
    $.ajax({
        url: admin_departments,
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
                    setTimeout(function () {
                        window.location.href = admin_departments;
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