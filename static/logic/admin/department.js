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
                    toastr.success(message, 'Success', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                    $("#BTNIcon").removeClass("fa-spinner fa-pulse fa-fw").addClass("fa-save");
                    document.getElementById("makeBTN").disabled = false;
                    setTimeout(function () {
                        window.location.href = admin_departments;
                    }, 2300);
                    
                }
                else if (status === 403) {
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