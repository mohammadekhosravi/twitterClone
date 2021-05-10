const tweetBtn = document.getElementById('create-tweet');
const submitTweetBtn = document.getElementById('tweet-submit');
const tweetForm = document.getElementById('tweet-form');
const csrf_token = document.getElementsByName('csrfmiddlewaretoken');
const body = document.getElementById('id_body')
// ----------------------------------------------------------------
const mentionBtn = document.getElementById('mention-button');
const mention = document.getElementById('id_mention');
const mentionForm = document.getElementById('mention-form');
const submitMentionBtn = document.getElementById('mention-submit');
const tweetURL = mentionForm.getAttribute('data-tweet');


// For tweet
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

// For mention
mentionBtn.addEventListener('click', function(e) {
    e.preventDefault();
    toggleModal('mention-modal');
})

submitMentionBtn.addEventListener('click', function(e) {
    e.preventDefault;
    
    $.ajax({
        type: 'POST',
        url: `/compose/${tweetURL}/mention/`,
        data: {
            'csrfmiddlewaretoken': csrf_token[0].value,
            'mention': mention.value,
        },
        success: function(response) {
            toggleModal('mention-modal');
            tweetForm.reset();
        },
        error: function(error) {
            alert("Oops something went wrong!");
        }
    })
})