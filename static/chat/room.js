const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    // document.querySelector('#chat-log').value = null;
    const data = JSON.parse(e.data);
    const messages = JSON.parse(data.messages)
    for (let i = 0; i < messages.length; i++) {
        const element = messages[i];
        const message = element.fields.content
        document.querySelector('#chat-log').value += (message + '\n');
        
    }
};
    

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'command':'send'
    }));
    messageInputDom.value = '';
};
chatSocket.onopen = function (){
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'command':'fetch',
        'message':message
    }))
}