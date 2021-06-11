let ws;
let url;



function initWebSocket() {
    try {
        ws = new WebSocket(url);
        console.log("WebSocket: ok" + url);
    } catch (e) {
        console.log(e.message);
    }
}

function addMessage(message) {
    if (message.length !== 0) {
        let tag = "<div class=\"message-right\">" + message + "</div>";
        console.log(tag);

        let container = document.querySelector("#message_container");
        container.innerHTML += tag;
        container.scrollTop = container.scrollHeight;
    }
}

function addMessageList(messages) {
    for (let message in messages) {
        addMessage(message);
    }
}

document.querySelector("#submit").
        addEventListener("click", function () {

            let input = document.querySelector("#message_input");
            addMessage(input.value);
            input.value = "";
        });

document.querySelector(".close_button").
        addEventListener("click", function () {
            let chat = document.querySelector(".chat");
            let button = document.querySelector(".chat_icon");

            chat.style.display = "none";
            button.style.display = "";
        });

document.querySelector(".chat_icon").
        addEventListener("click", function () {
            let chat = document.querySelector(".chat");
            let button = document.querySelector(".chat_icon");

            chat.style.display = "";
            button.style.display = "flex";
        });

document.querySelector(".chat_icon").
        addEventListener("mouseover", function () {
            let button = document.querySelector(".chat_icon");
            button.style.boxShadow = "0 0 20px 0 #0db79b";
        });

document.querySelector(".chat_icon").
        addEventListener("mouseout", function () {
           let button = document.querySelector(".chat_icon");
           button.style.boxShadow = "";
        });