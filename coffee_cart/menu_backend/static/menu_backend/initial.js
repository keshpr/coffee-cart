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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).ready(function () {
    console.log("Here")
    $.ajax({
        url: 'http://192.168.99.100:8000/api/v1/menu/getItem/second_item',
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            "name": "second_item",
            "ingredients": ["ingr3", "ingr4"],
            "type": "drink",
            "well_with": ["first_item"]
        }),
        success: function (data) {
            $("p").text(JSON.stringify(data));
        }
    })
});