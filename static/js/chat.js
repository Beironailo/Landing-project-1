let userWebSocket;
let adminWebSocket;

function initWebSocket(url) {

    try {

        userWebSocket = new WebSocket(url);
        adminWebSocket = new WebSocket(
            "ws://" + window.location.host + "/ws/chat/"
        );

        adminWebSocket.onopen = userWebSocket.onopen = function () {

            console.log("WebSocket opened");

        }

        adminWebSocket.onclose = userWebSocket.onclose = function (event) {

            console.log("WebSocket closed: " + event.code);

        }

        adminWebSocket.onerror = userWebSocket.onerror = function (error) {

            console.log("WebSocket died:" + error.message);

        }

        userWebSocket.onmessage = function (event) {

            let eventObject = JSON.parse(event.data);

            addMessage(eventObject);

        }

    } catch (e) {

        console.log(e.message);

    }
}

function addMessage(message) {

    if (message.text.length !== 0) {

        let tag;
        if (message.user === "Guest") {

            tag = "<div class=\"message-right\">" + message.text + "</div>";

        } else {

            tag = "<div class=\"message-left\">" + message.text + "</div>";

        }

        let container = document.querySelector("#message_container");
        container.innerHTML += tag;
        container.scrollTop = container.scrollHeight;

    }
}

document.querySelector("#submit")
    .addEventListener("click", function () {

        let input = document.querySelector("#message_input");
        let now = new Date();

        let message = {
            date: now.getHours().toString() + ":" + now.getMinutes().toString(),
            text: input.value
        };
        let json = {
            date: message.date,
            text: message.text
        }
        let adminJson = {
            date: message.date,
            text: message.text,
            room: document.querySelector("#room_name").innerHTML.trim()
        }

        try {

            userWebSocket.send( JSON.stringify(json) );
            adminWebSocket.send( JSON.stringify(adminJson) );

        } catch (e) {

            console.log(e.message);

        }

        console.log( JSON.stringify(json) )
        console.log( JSON.stringify(adminJson) );

        input.value = "";

    });

document.querySelector(".close_button")
    .addEventListener("click", function () {

        let chat = document.querySelector(".chat");
        let button = document.querySelector(".chat_icon");

        chat.style.display = "none";
        button.style.display = "";

    });


document.querySelector(".chat_icon")
    .addEventListener("mouseover", function () {

        let button = document.querySelector(".chat_icon");
        button.style.boxShadow = "0 0 20px 0 #0db79b";

    });

document.querySelector(".chat_icon")
    .addEventListener("mouseout", function () {

        let button = document.querySelector(".chat_icon");
        button.style.boxShadow = "";

    });

document.querySelector(".chat_icon")
    .addEventListener("click", function () {

        if (userWebSocket == null) {
            let room = document.querySelector("#room_name").innerHTML.trim();
            let url = 'ws://'
                + window.location.host
                + '/ws/chat/'
                + room
                + '/'

            console.log(url);
            initWebSocket(url);
        }

        let chat = document.querySelector(".chat");
        let button = document.querySelector(".chat_icon");

        chat.style.display = "";
        button.style.display = "flex";

    });
