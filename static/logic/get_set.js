//Change 2FA State
function change() {
    var two_fa = document.getElementById('two_fa');
    var two_fa_state = "";
    if(two_fa.checked){
        two_fa_state = 1;
    } else {
        two_fa_state = 0;
    }
    var payload = { two_fa_state: two_fa_state };
    if (two_fa_state == 1)
    {
        $.ajax({
            url: get_set_two_fa,
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
                            window.location.href = admin_settings;
                        }, 2300);
                        
                    }
                    else {
                        toastr.warning('That Did Not Work, Try Again.', 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                        setTimeout(function () {
                            window.location.href = admin_settings;
                        }, 2300);
                    }
                }
            }
        });
    }
    else
    {
        swal({
            title: "Are you sure?",
            text: "Your Account Will No Be Protected By 2FA",
            icon: "warning",
            showCancelButton: true,
            buttons: {
                cancel: {
                    text: "Cancel",
                    value: null,
                    visible: true,
                    className: "",
                    closeModal: true,
                },
                confirm: {
                    text: "Yes, Disable",
                    value: true,
                    visible: true,
                    className: "btn-warning",
                    closeModal: false
                }
            }
        })
        .then((isConfirm) => {
            if (isConfirm) {
                swal.close()
                $.ajax({
                    url: get_set_two_fa,
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
                                    window.location.href = admin_settings;
                                }, 2300);
                                
                            }
                            else {
                                toastr.warning('That Did Not Work, Try Again.', 'Warning', { "closeButton": true, "showMethod": "slideDown", "hideMethod": "fadeOut", timeOut: 2000 });
                                setTimeout(function () {
                                    window.location.href = admin_settings;
                                }, 2300);
                            }
                        }
                    }
                });
            } 
            else {
                swal.close()
            }
        });
    }

}