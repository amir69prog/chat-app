var endpoint = 'ws://' + window.location.host + '/' + 'friends/';
const friendSocket = new WebSocket(endpoint);




friendSocket.onclose = function (e) {
    console.log(e)
}

friendSocket.onerror = function (e) {
    console.log(e)
}


friendSocket.onmessage = function (event) {
    console.log(event)
    data = JSON.parse(event.data)
    location.reload();
    return false;
}

function remove_friend(friend) {
    // remove freind fromfriend list
    let data = {
        'action':'remove',
        'friend':friend
    }
    friendSocket.send(JSON.stringify(data));
};
