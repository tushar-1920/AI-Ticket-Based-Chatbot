const socket = io();

const chatBox = document.getElementById("chat-box");

const typingIndicator = document.getElementById("typing");


// SEND MESSAGE

function sendMessage()
{
    const input = document.getElementById("message-input");

    const message = input.value.trim();

    if(!message)
    {
        return;
    }

    if(!window.currentConversationId)
    {
        alert("No conversation selected");
        return;
    }

    addMessage("user", message);

    showTyping();

    socket.emit("send_message", {

        message: message,

        conversation_id: window.currentConversationId

    });

    input.value = "";
}


// RECEIVE MESSAGE

socket.on("receive_message", function(data)
{
    hideTyping();

    streamBotMessage(data.message);
});


// ADD MESSAGE (USER OR BOT)

function addMessage(sender, text)
{
    const div = document.createElement("div");

    div.className = "message " + sender;

    const avatar =
        sender === "user"
        ? "/static/img/user.png"
        : "/static/img/bot.png";

    const time = new Date().toLocaleTimeString();

    div.innerHTML = `
        <img src="${avatar}">
        <div class="message-content">
            <div class="message-text">${text}</div>
            <div class="timestamp">${time}</div>
        </div>
    `;

    chatBox.appendChild(div);

    scrollDown();
}


// STREAM BOT MESSAGE (PROFESSIONAL)

function streamBotMessage(text)
{
    const div = document.createElement("div");

    div.className = "message bot";

    const avatar = "/static/img/bot.png";

    const time = new Date().toLocaleTimeString();

    div.innerHTML = `
        <img src="${avatar}">
        <div class="message-content">
            <div class="message-text" id="stream-text"></div>
            <div class="timestamp">${time}</div>
        </div>
    `;

    chatBox.appendChild(div);

    const textElement = div.querySelector("#stream-text");

    let i = 0;

    const interval = setInterval(() =>
    {
        if(i >= text.length)
        {
            clearInterval(interval);
            return;
        }

        textElement.innerText += text[i];

        i++;

        scrollDown();

    }, 20);
}


// SHOW TYPING

function showTyping()
{
    typingIndicator.style.display = "block";
}


// HIDE TYPING

function hideTyping()
{
    typingIndicator.style.display = "none";
}


// LOAD MESSAGES

function loadMessages(conversationId)
{
    fetch("/conversation/messages/" + conversationId)
    .then(res => res.json())
    .then(data =>
    {
        chatBox.innerHTML = "";

        data.forEach(msg =>
        {
            addMessage(msg.sender, msg.message);
        });
    });
}


// SCROLL

function scrollDown()
{
    chatBox.scrollTop = chatBox.scrollHeight;
}


// LOAD ON START

window.addEventListener("load", () =>
{
    if(window.currentConversationId)
    {
        loadMessages(window.currentConversationId);
    }
});