let websocket;

function initWebSocket(url) {

    try {

        websocket = new WebSocket(url);

        websocket.onopen = function () {

            console.log("WebSocket opened");

        }

        websocket.onclose = function (event) {

            console.log("WebSocket closed: " + event.code);

        }

        websocket.onerror = function (error) {

            console.log("WebSocket died:" + error.message);

        }

        websocket.onmessage = function (event) {

            let text = event.data.text;
            let date = event.data.date;

            addMessage(text,  "L");

        }

    } catch (e) {

        console.log(e.message);

    }
}

function addMessage(message, source) {

    if (message.text.length !== 0) {

        let tag;
        if (source === "R") {

            try {

                let json = {
                    date: message.date,
                    text: message.text
                }

                websocket.send( JSON.stringify(json) );

                tag = "<div class=\"message-right\">" + message.text + "</div>";

            } catch (e) {

                console.log(e.message);

            }

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
        addMessage({
            date: now.getHours().toString() + ":" + now.getMinutes().toString(),
            text: input.value
        }, "R");
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

        if (websocket == null) {
            let room = document.querySelector("#room_name").innerHTML;
            let url = "ws://"
                + window.location.host
                + "/ws/chat/"
                + room
                + "/"
            initWebSocket(url);
        }

        let chat = document.querySelector(".chat");
        let button = document.querySelector(".chat_icon");

        chat.style.display = "";
        button.style.display = "flex";

    });
