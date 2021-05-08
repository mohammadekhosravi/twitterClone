const followBtn = document.getElementById("follow-button");
const userId = followBtn.getAttribute('data-id');
const userAction = followBtn.getAttribute('data-action');
const url = followBtn.getAttribute("data-url");
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const getCookie =(name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

followBtn.addEventListener("click", (e) => {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrftoken,
            id: userId,
            action: userAction,
        },
        success: function(respose){
            if (respose.status == 'ok'){
                followBtn.innerText = "Following";
            }
            else if(respose.status == 'error'){
                alert("Oops! something went wrong!");
            }
        },
        error: function(error){
            alert(error)
        }
    })
})