var endpoint = 'ws://' + window.location.host + '/' + 'request/';
const requestSocket = new WebSocket(endpoint);


requestSocket.onclose = function (e) {
    console.log(e)
}

requestSocket.onerror = function (e) {
    console.log(e)
}


requestSocket.onmessage = function (event) {
    console.log(event)
    data = JSON.parse(event.data)
    location.reload();
    return false;
}



function send_request(receiver) {
    console.log('create')
    // create a request from current user and receiver
    let data = {
        'action':'send',
        'receiver':receiver
    }
    requestSocket.send(JSON.stringify(data));
};


function accept_request(sender) {
    console.log('accept')
    // accept a request from current user and sender
    let data = {
        'action':'accept',
        'sender':sender
    }
    requestSocket.send(JSON.stringify(data));
};


function cancel_request(receiver) {
    console.log('cancel')
    // cancel a request from current user and receiver
    let data = {
        'action':'cancel',
        'receiver':receiver
    }
    requestSocket.send(JSON.stringify(data));
};


function decline_request(sender) {
    console.log('decline')
    // decline a request from current user and sender
    let data = {
        'action':'decline',
        'sender':sender
    }
    requestSocket.send(JSON.stringify(data));
};