let url = 'ws://' + document.location.host + '/' + 'private' + document.location.pathname;
const socket = new WebSocket(url)

$(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(function() {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function() {
	$("#profile-img").removeClass();
	$("#status-online").removeClass("active");
	$("#status-away").removeClass("active");
	$("#status-busy").removeClass("active");
	$("#status-offline").removeClass("active");
	$(this).addClass("active");
	
	if($("#status-online").hasClass("active")) {
		$("#profile-img").addClass("online");
	} else if ($("#status-away").hasClass("active")) {
		$("#profile-img").addClass("away");
	} else if ($("#status-busy").hasClass("active")) {
		$("#profile-img").addClass("busy");
	} else if ($("#status-offline").hasClass("active")) {
		$("#profile-img").addClass("offline");
	} else {
		$("#profile-img").removeClass();
	};
	
	$("#status-options").removeClass("active");
});

socket.onmessage = function(event){
	let data = JSON.parse(event.data)
	const user = data.message.author
	const picture_url = data.message.profile_picture
	const message = data.message.content
	if (data.action == 'new_message')
		newMessage(user,picture_url,message)
}


function newMessage(user,picture_url,message) {
	const url = document.location.pathname;
	const username = url.split("/").pop();
	if ( user == username) {
		$('<li class="sent"><img src="' + picture_url + '" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
		$('.contact.active .preview').html(message);
	} else {
		$('<li class="replies"><img src="' + picture_url + '" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
		$('.contact.active .preview').html(message);
	}
	$('.message-input input').val(null);
	// $(".messages").animate({ scrollTop: $(document).height() }, "fast");
}


function sendMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
	let data = {
		'type':'send_message',
		'message':message
	}
	socket.send(JSON.stringify(data))
};


$('.submit').click(function() {
	sendMessage();
  });
  
$(window).on('keydown', function(e) {
if (e.which == 13) {
	sendMessage();
	return false;
}
});

function chat_private(username) {
	window.location.pathname = '/chat/' + username ;
};