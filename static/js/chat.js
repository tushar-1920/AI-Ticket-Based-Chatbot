const socket = io();

function sendMessage() {

    const input = document.getElementById("message-input");

    const message = input.value;

    if (!message) return;

    addUserMessage(message);

    socket.emit("send_message", {
        message: message
    });

    input.value = "";
}


socket.on("receive_message", function(data) {

    showTyping();

    setTimeout(() => {

        hideTyping();

        addBotMessage(data.message);

    }, 1000);

});

function showTyping(){

const chatBox = document.getElementById("chat-box");

const div = document.createElement("div");

div.id = "typing";

div.innerText = "AI is typing...";

chatBox.appendChild(div);

}

function hideTyping(){

let typing = document.getElementById("typing");

if(typing) typing.remove();

}

function addUserMessage(message) {

    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerText = message;

    chatBox.appendChild(div);

}


function addBotMessage(message) {

    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerText = message;

    chatBox.appendChild(div);

}