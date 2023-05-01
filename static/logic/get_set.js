// 2FA Check
$(document).ready(function () {
    // 
    $.ajax({
        url: get_set_two_fa,
        type: "GET",
        dataType: "json",
        headers: {
            content_type: 'application/json',
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            if (data) {
                var status = data.status
                if (status) {
                    $("#two_fa").prop("checked", true);
                }
                else {
                    $("#two_fa").prop("checked", false);
                }
            }
        }
    });
});

//Change 2FA State
function change() {
    var two_fa = document.getElementById('two_fa');
    var two_fa_state = "";
    if(two_fa.checked){
        two_fa_state = 'Checked';
    } else {
        two_fa_state = 'UnChecked';
    }
    alert(two_fa_state);
}