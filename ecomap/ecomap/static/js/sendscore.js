//gets cookie based on name (used for getting csrf token)
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



function sendScore(score)
{
    var csrftoken = getCookie('csrftoken');
    //sends POST request to sendScore with csrfttoken and score
    $.ajax({
        type: "POST",
        url: '/sendScore/',
        data: {
            "score": score,
            'csrfmiddlewaretoken': csrftoken,
        },
        dataType: "json",
        success: function(data){
            console.log("Sent Score")
        },
        failure: function(){
            console.log("Did not send Score")
        }
    });
}

function deleteSelfAccount(password)
{
    var csrftoken = getCookie('csrftoken');
    //sends POST request to sendScore with csrfttoken and score
    $.ajax({
        type: "POST",
        url: '/deleteSelfAccount/',
        data: {
            "password": password,
            'csrfmiddlewaretoken': csrftoken,
        },
        dataType: "json",
        success: function(data){
            window.location.href = "/login/";
            return true;
        },
        failure: function(){
            window.location.href = "/profile/";
            return false;
        }
    });
}