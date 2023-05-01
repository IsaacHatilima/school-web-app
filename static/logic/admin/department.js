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
                if (status === 201) {
                    toastr.success(message, 'Success', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("makeBTN").disabled = false;
                    setTimeout(function () {
                        window.location.href = admin_departments;
                    }, 2300);
                    
                }
                else if (status === 302) {
                    toastr.warning(message, 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
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

function update_click(clicked_id)
{ 
    document.getElementById(clicked_id).disabled = true;
    let icon = '#BTNIcon_' + clicked_id
    $(icon).removeClass("fa-save").addClass("fa-spinner fa-pulse fa-fw");
    let department = $("#department_" + clicked_id).val();
    var payload = { department: department };
    const error_msg = document.getElementById('error_msg')
    if (department == null || department == '')
    {
        $("#department_" + clicked_id).removeClass("border-primary").addClass("border-danger");
        error_msg.style.display = "block";
        $(icon).removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
        document.getElementById(clicked_id).disabled = false;
    }
    else {
        $(icon).removeClass("fa-save").addClass("fa-spinner fa-pulse fa-fw");
        document.getElementById(clicked_id).disabled = true;
        $("#department_" + clicked_id).removeClass("border-danger").addClass("border-primary");
        error_msg.style.display = "none";
        $.ajax({
            url: admin_dept_details+clicked_id+'/',
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
                        toastr.success(message, 'Success', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                        setTimeout(function () {
                            window.location.href = admin_departments;
                        }, 2300);
                        
                    }
                    else {
                        toastr.warning('That Did Not Work, Try Again.', 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                        $(icon).removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                        document.getElementById(clicked_id).disabled = false;
                    }
                }
            },
            error: function () {
                toastr.error('Internal Server Error!', 'Error', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                $(icon).removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                document.getElementById(clicked_id).disabled = false;
            }
        });       
    }

}

function delete_click(clicked_id)
{ 
    let id = clicked_id.slice(4);
    console.log(id)
    document.getElementById(clicked_id).disabled = true;
    let icon = '#del_BTNIcon_' + id
    $(icon).removeClass("fa-trash").addClass("fa-spinner fa-pulse fa-fw");
    let department = $("#department_" + id).val();
    var payload = { department: department };
    $.ajax({
        url: admin_dept_details+id+'/',
        data: payload,
        type: "DELETE",
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
                    setTimeout(function () {
                        window.location.href = admin_departments;
                    }, 2300);
                    
                }
                else {
                    toastr.warning('That Did Not Work, Try Again.', 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $(icon).removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById(clicked_id).disabled = false;
                }
            }
        },
        error: function () {
            toastr.error('Internal Server Error!', 'Error', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
            $(icon).removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
            document.getElementById(clicked_id).disabled = false;
        }
    }); 

}