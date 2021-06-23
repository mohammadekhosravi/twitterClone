const followBtn = document.getElementById("follow-button");
const userId = followBtn.getAttribute('data-id');
let userAction = followBtn.getAttribute('data-action');
const url = followBtn.getAttribute("data-url");
const csrf = document.getElementsByName('csrfmiddlewaretoken');
let followersCount = document.getElementById("fuck");

function goBack() {
    window.history.back();
}


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
        success: function(response){
            pervious_action = userAction;
            if (response.status == 'ok'){
                followBtn.innerText = pervious_action == 'follow' ? "Following" : "Follow";
                if(pervious_action == 'follow') {
                    followBtn.classList.replace("bg-transparent", "bg-blue-500");
                    followBtn.classList.replace("text-blue-500", "text-white");
                }
                else {
                    followBtn.classList.replace("bg-blue-500", "bg-transparent");
                    followBtn.classList.replace("text-white", "text-blue-500");
                    followersCount.innerText -= 1;
                }
                followersCount.innerText = response.followers_count;
                userAction = pervious_action == 'follow' ? "unfollow" : "follow";
            }
            else if(response.status == 'error'){
                alert("Oops! something went wrong!");
            }
        },
        error: function(error){
            alert(error)
        }
    })
})
