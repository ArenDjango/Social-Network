$(document ).ready(function(){
    var block = document.getElementById("messpanelchild");
  block.scrollTop = 9999;
});

$('#chat-form').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : '/post/{{ userobjchat.id }}/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val() },

        success : function(json){
            $('#chat-msg').val('');
        $('#msg-list').append('<li class="text-right mymsg">' + 
            '<p class="pright">' +
            json.msg + 
            '<br>' +
            '<small>' +
            '...' +
            '<a class="menuclassmessage" href="/chatdel/{{ mess.id }}/"> ' +
            '<i class="fas fa-trash-alt"></i>' +
            '</a>' +
            '</small>' +
            '</p>' +
            '</li>');
            var block = document.getElementById("messpanelchild");
  block.scrollTop = 9999;
        }
    });
});


              



function getMessages(){
    if (!scrolling) {
    $.get('/messages/{{ userobjchat.id }}', function(messages){
            $('#msg-list').html(messages);
        var block = document.getElementById("messpanelchild");
  if (block.scrollTop > 9998){
    block.scrollTop = 9999;
  }
});
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#messagepole').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 500);
});

$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
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


