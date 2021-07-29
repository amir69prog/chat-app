const roomName = JSON.parse(document.getElementById('room-name').textContent);
console.log(roomName)
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onopen = function (e) {

}

chatSocket.onmessage = function(event){
	let data = JSON.parse(event.data)
    console.log(data)
	const user = data.message.author
	const picture_url = data.message.profile_picture
	const message = data.message.content
    const current_user = JSON.parse(document.getElementById('current_user').textContent);
	newMessage(user,picture_url,message,current_user)
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


function newMessage(user,picture_url,message,current_user) {
	if ( user == current_user) {
		$('<li class="sent"><img src="' + picture_url + '" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	} else {
		$('<li class="replies"><img src="' + picture_url + '" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	}
	$('.message-input input').val(null);
	window.scrollTo(0,document.body.scrollHeight);


}


function sendMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
	let data = {
		'message':message,
		'command':'send'
	}
	chatSocket.send(JSON.stringify(data))
};


$(window).on('keydown', function(e) {
if (e.which == 13) {
	sendMessage();
    console.log('hey')
	return false;
}
});