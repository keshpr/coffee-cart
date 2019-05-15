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



function getBody(){
    var body = {};
    body.name = $("#name").val();
    body.type = $("#item-type").text();
    body.ingredients = [];
    $.each($(".ingr"), function(){
        var ingrName = $(this).find(".ingr-name").text();
        body.ingredients.push(ingrName);
    });
    body.well_with = [];
    $.each($(".side"), function(){
        var sideName = $(this).find(".side-name").text();
        body.well_with.push(sideName);
    });
    return body;
}


function addMessage(data){
    console.log('Adding message');
    var mess = "<strong>";
    if(data.success){
        mess += "Success!"
    }else if(data.error){
        mess += "Error: " + data.error;
    }
    mess += "</strong>"
    $("#message").append(mess);
}

$(document).ready(function () {
    console.log("Here")
    
    $(document).on('click', '.remove-button', function(){
        console.log('removing')
        console.log($(this).parent().prop('nodeName'));
        $(this).parent().remove();
    });
    
    $("#add-button-ingr").on('click', function(){
        console.log("Adding ingredient");
        var ingr = $(this).prev().prev().val()
        $(this).parent().prev().append("<div class='ingr'><div class='ingr-name'>" + ingr + "</div><button type='button' class='remove-button'>Remove</button></div><br>");
    });
    
    $('#add-button-side').click(function(){
        $.each($("#select-side option:selected"), function(){
            var side = $(this).val();
            $("#list-of-sides").append("<div class='side'><div class='side-name'>" + side + "</div><button type='button' class='remove-button'>Remove</button></div><br></br>")
        });
    });
    $("#add-form").submit(function(event){
        console.log("Sending")
        var body = getBody();
        console.log(body)
        $.ajax({
            url: 'http://192.168.99.100:8000/api/v1/menu/addItem/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(body),
            success: function (data) {
                console.log(data);
                addMessage(data);
            }
        })
        event.preventDefault();
    });
    $("#update-form").submit(function(event){
    
        var body = getBody();
        $.ajax({
            url: 'http://192.168.99.100:8000/api/v1/menu/updateItem/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(body),
            success: function (data) {
                console.log("Updated??")
                console.log(data);
                addMessage(data);
            }
        })
        event.preventDefault();
    });
    
});