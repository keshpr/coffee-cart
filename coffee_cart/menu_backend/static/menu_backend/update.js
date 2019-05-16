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
    body.oldname = $("#oldname").val();
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

function checkBody(body){
    if(body.name.length == 0){
        console.log("Not allowed")
        addMessage({'error': 'Item name cannot be empty!'});
        event.preventDefault();
        return false;
    }
    if(body.ingredients == []){
        addMessage({'error': 'Item must have some ingredients!'});
        event.preventDefault();
        return false;
    }
    return true;
}

function addMessage(data){
    console.log('Adding message');
    var mess = ""
    if(data.success){
        mess += "Success!"
        $('#message').attr('style', 'color:green');
    }else if(data.error){
        mess += "Error: " + data.error;
        $('#message').attr('style', 'color:red');
    }
    $("#message").text(mess);
    window.scrollTo(0,0);
}

$(document).ready(function () {
    $(document).on('click', '.remove-button', function(){
        $(this).parent().remove();
    });
    
    $("#add-button-ingr").on('click', function(){
        var ingr = $(this).prev().prev().val()
        $(this).parent().prev().append("<li class='ingr'><span class='ingr-name'>" + ingr + "</span><button type='button' class='remove-button'>Remove</button></li>");
    });
    
    $('#add-button-side').click(function(){
        $.each($("#select-side option:selected"), function(){
            var side = $(this).val();
            $("#list-of-sides").append("<li class='side'><span class='side-name'>" + side + "</span><button type='button' class='remove-button'>Remove</button></li>")
        });
    });
    $(".add-form").submit(function(event){
        var body = getBody();
        if(! checkBody(body)){
            return
        }
        $.ajax({
            url: 'http://192.168.99.100:8000/api/v1/menu/addItem/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(body),
            success: function (data) {
                addMessage(data);
            }
        })
        event.preventDefault();
    });
    $(".update-form").submit(function(event){
    
        var body = getBody();
        if(! checkBody(body)){
            return
        }
        $.ajax({
            url: 'http://192.168.99.100:8000/api/v1/menu/updateItem/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(body),
            success: function (data) {
                addMessage(data);
            }
        })
        event.preventDefault();
    });
    
});