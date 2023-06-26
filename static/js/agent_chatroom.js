let wsStart = 'ws://'
if(window.location.protocol === 'https'){
  wsStart = 'wss://'
}
let chatGuest = ''

let chatSocket = null


const CurrentSite = document.querySelector('#site').textContent.replaceAll('"', '')
console.log('CurrentSite  :', CurrentSite)
const roomNameElement = document.querySelector('#room_name').textContent.replaceAll('"', '')
console.log('roomNameElement  :', roomNameElement)
const chatSubmitElement = document.querySelector('#sendmessagebutton')
// console.log('chatSubmitElement  :', chatSubmitElement)
const messageElement = document.querySelector('#message_input')
// console.log('messageElement  :', messageElement)
const guestElement = document.querySelector('#guest')
// console.log('guestElement  :', guestElement)
const agentNameElement = document.querySelector('#agent_name').textContent.replaceAll('"', '')
// console.log('agentNameElement  :', agentNameElement)
const agentIdElement = document.querySelector('#agent_id').textContent.replaceAll('"', '')
// console.log('agentIdElement  :', agentIdElement)
const chatLogElement = document.querySelector('#chat_log')
// console.log('chatLogElement  :', chatLogElement)



function scrollToBottom(){
  chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
      'type':'message',
      'message': messageElement.value,
      'guest': chatGuest,
      'agent': agentNameElement,
      'agentid': agentIdElement,
      'site': CurrentSite,
    }))
    messageElement.value = ''
  }
  

function OnChatMessage(data){

    if (data.type === "chat_message"){
      if (data.guest){
        chatLogElement.innerHTML += `
          <div class="wt-offerermessage">
            <figure>
              <img src="/static/images/user-login.jpg/" alt="image description">
            </figure>
            <div class="wt-description">
              <div class="clearfix"></div>
              <p>${data.message} </p>
              <div class="clearfix"></div>
              <p style="padding:2px; margin:0 font-size:10px;">Sent by: ${data.guest}</p>
              <time datetime="2017-08-08">${data.created_at} ago</time>
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
              <p style="padding:2px; margin:0; font-size:10px;">Sent by: ${data.agent}</p>
              <time datetime="2017-08-08">${data.created_at} ago</time>
            </div>
          </div>`
      }
    }
    scrollToBottom()
  }


chatSocket = new WebSocket(`${wsStart}${window.location.host}/ws/${roomNameElement}/?site=${CurrentSite}`)
chatSocket.onmessage = function(e){

  console.log('on message stage')
  OnChatMessage(JSON.parse(e.data))
  scrollToBottom()
  return false
}
chatSocket.onopen = function(e){
  console.log('on open stage')
  scrollToBottom()
}
chatSocket.onclose = function(e){
  console.log('on close stage')
}


chatSubmitElement.onclick = function(e){
    e.preventDefault()
    
    sendMessage()
  
    return false
  }

  
messageElement.onkeyup = function(e){
  if(e.keyCode == 13){
    sendMessage()
  }
}