function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// retrieve new container with entries
function get_content(url, object_id) {
    var result;
    $.ajax({
        method: 'POST',
        url: url,
        headers: {'X-CSRFToken': getCookie('csrftoken'), 'X-Frame-Options': 'DENY'},
        data: {'entry_id': object_id}
        }).done(function(data, status, request_obj) {
            $('.entry_container').replaceWith(data);
        });
}

// roller buttons
function roller_bk() {
    var end_id = $('.roller-end-id').val();
    get_content('/get_prev', end_id);
}

function roller_fwd() {
    var start_id = $('.roller-start-id').val();
    get_content('/get_next', start_id);
}


$(document).ready(function() {

    var messages_ttl = $('.messages_ttl').val() * 1000;

    // events
    // highlight roller buttons
    $('.btn-back, .btn-fwd')
        .mouseover(
            function() {
            $(this).css({'background': 'violet', 'cursor': 'pointer'});
            }
        ).mouseout(
            function() {
            $(this).css('background', 'thistle');
            }
        );

    // show selector if "pinned" unmarked
    $('.pinned').change(function() {
        if (this.checked === false) {
            $('.delete_after').css('display', 'block');
        } else {
            $('.delete_after').css('display', 'none');
        }
    });

    // clear messages after "messages_ttl" sec.
    var message = $('.green_message').text();
    if (message.length > 0) {
        setTimeout(function() {
            $('.green_message').text('');
            }, messages_ttl);
    }
});