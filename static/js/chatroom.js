let wsStart = 'ws://'
if(window.location.protocol === 'https'){
  wsStart = 'wss://'
}
let chatGuest = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatReference = Math.random().toString(36).slice(2,12)


const chatOpenElement = document.querySelector('#wt-getsupport')
const chatOpenDivElement = document.querySelector('#showOpenChat')
const chatOpenButtonElement = document.querySelector('#open_button')
const chatHideDivElement = document.querySelector('#hideOpenChat')
const WelcomeGuestDivElement = document.querySelector('#welcomeGuest')
const chatSubmitElement = document.querySelector('#sendmessagebutton')
const roomNameElement = document.querySelector('#room_name')
const messageElement = document.querySelector('#message_input')
const guestElement = document.querySelector('#guest')
const chatLogElement = document.querySelector('#chat_log')



function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
// let csrftoken = getCookie('csrftoken');


function sendMessage(){
  chatSocket.send(JSON.stringify({
    'type':'message',
    'message': messageElement.value,
    'guest': chatGuest,
  }))
  messageElement.value = ''
}


function OnChatMessage(data){

  if (data.type === "chat_message"){
    if (data.agent){
      chatLogElement.innerHTML += `
        <div class="wt-offerermessage">
          <figure>
            <img src="/static/images/user-login.jpg/" alt="image description">
          </figure>
          <div class="wt-description">
            <div class="clearfix"></div>
            <p>${data.message} </p>
            <div class="clearfix"></div>
            <time>by: ${data.guest}</time>
          </div>
        </div>`
    }else{
       
      chatLogElement.innerHTML += `
        <div class="wt-memessage wt-readmessage">
          <figure>
            <img src="/static/images/user-login.jpg/" alt="image description">
          </figure>
          <div class="wt-description">
            <div class="clearfix"></div>
            <p>${data.message} </p>
            <div class="clearfix"></div>
            <time>by: ${data.guest}</time>
            </div>
            </div>`
            // <p>${data.guest}</p>
            // <time datetime="2017-08-08">Time: ${data.created_at}</time>
    }
  }
}

// Function for joining chatroom
async function joinChatroom(){

  chatGuest = guestElement.value;

  const data = {
    'reference': chatReference,
    'guestname': chatGuest,
    'url': chatWindowUrl,
  }

  await fetch(`/ws/create-room/${chatReference}/`,{
    method :'POST',
    headers:{
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    credentials: 'same-origin',
    body: JSON.stringify(data)
  })
  .then(function(res){
    return res.json()
  })
  .then(function(data){
    console.log('data', data)
  })
  .catch(function (error) {
    console.log(error)
  })

  chatSocket = new WebSocket(`${wsStart}${window.location.host}/${chatReference}/`)
  chatSocket.onmessage = function(e){

    console.log('on message stage')
    OnChatMessage(JSON.parse(e.data))

    return false
  }
  chatSocket.onopen = function(e){
    console.log('on open stage')
    // sendMessage()
  }
  chatSocket.onclose = function(e){
    console.log('on close stage')
  }
}

chatOpenElement.onclick = function(e){
  e.preventDefault()
  chatOpenDivElement.classList.remove('hidden')
  
  return false
}

chatOpenButtonElement.onclick = function(e){
  e.preventDefault()
  
  chatOpenDivElement.classList.add('hidden')
  chatHideDivElement.classList.remove('hidden')
  WelcomeGuestDivElement.textContent = 'Welcome ' + guestElement.value

  joinChatroom()
  return false
}

chatSubmitElement.onclick = function(e){
  e.preventDefault()
  
  sendMessage()

  return false
}