const tweetBtn = document.getElementById('create-tweet');
const submitTweetBtn = document.getElementById('tweet-submit');
const tweetForm = document.getElementById('tweet-form');
const csrf_token = document.getElementsByName('csrfmiddlewaretoken');
const body = document.getElementById('id_body')


tweetBtn.addEventListener('click', function(e){
    e.preventDefault();
    toggleModal('modal-id');
})

submitTweetBtn.addEventListener('click', function(e) {
    e.preventDefault;
    
    $.ajax({
        type: 'POST',
        url: '/compose/tweet/',
        data: {
            'csrfmiddlewaretoken': csrf_token[0].value,
            'body': body.value,
        },
        success: function(response) {
            toggleModal('modal-id');
            tweetForm.reset();
        },
        error: function(error) {
            alert("Oops something went wrong!");
        }
    })
})

function toggleModal(modalID){
    document.getElementById(modalID).classList.toggle("hidden");
    document.getElementById(modalID + "-backdrop").classList.toggle("hidden");
    document.getElementById(modalID).classList.toggle("flex");
    document.getElementById(modalID + "-backdrop").classList.toggle("flex");
}