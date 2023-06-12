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

//Submit Form
$('#memeber_staff').submit(function (e) {
    e.preventDefault();
    // Disable Submit Button
    document.getElementById("makeBTN").disabled = true;
    // Switch button icon to loading Icon
    $("#BTNIcon").removeClass("fa-save").addClass("fa-spinner fa-pulse fa-fw");
    // Get input value
    var form = $(this);
    // Make payload
    $.ajax({
        url: admin_make_staff,
        data: form.serialize(),
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
                if (status === 201) {
                    toastr.success(message, 'Success', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("makeBTN").disabled = false;
                    setTimeout(function () {
                        window.location.href = admin_make_staff;
                    }, 2300);
                    
                }
                else {
                    toastr.warning('Account Creation Failed. Try Again', 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("makeBTN").disabled = false;
                }
            }
        },
        error: function () {
            toastr.error('Internal Server Error!', 'Error', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
            $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
            document.getElementById("makeBTN").disabled = false;
        }
    });
})

//Update User
$('#update_staff').submit(function (e) {
    e.preventDefault();
    //Get User ID for URL
    let userID = $('#user_id').val();
    // Disable Submit Button
    document.getElementById("updateBTN").disabled = true;
    // Switch button icon to loading Icon
    $("#BTNIcon").removeClass("fa-save").addClass("fa-spinner fa-pulse fa-fw");
    // Get input value
    var form = $(this);
    // Make payload
    $.ajax({
        url: admin_update_staff+userID+'/',
        data: form.serialize(),
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
                    toastr.success(message, 'Success', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("updateBTN").disabled = false;
                    setTimeout(function () {
                        window.location.href = admin_make_staff;
                    }, 2300);
                    
                }
                else {
                    toastr.warning(message, 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("updateBTN").disabled = false;
                }
            }
        },
        error: function () {
            toastr.error('Internal Server Error!', 'Error', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
            $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
            document.getElementById("updateBTN").disabled = false;
        }
    });
})

