let chatHistory = [];

async function sendMessage() {

    let input = document.getElementById("message");
    let message = input.value.trim();
    if (!message) return;

    // 1️⃣ add user message
    addMessage("user", message);

    chatHistory.push({ type: "user", message: message });
    saveChat();

    input.value = "";

    let chatArea = document.getElementById("chat-area");

    // 2️⃣ typing indicator (HERE is correct place)
    let typingDiv = document.createElement("div");
    typingDiv.className = "bot-msg";
    typingDiv.id = "typing";
    typingDiv.innerHTML = `
    <div class="typing">
        <span></span>
        <span></span>
        <span></span>
    </div>
`;


    chatArea.appendChild(typingDiv);

    // 3️⃣ call backend
    let response = await fetch("https://manojkumarpyapli-portfolio.onrender.com/chat?msg=" + message)


    let data = await response.json();

    // 4️⃣ delay for natural feel
    setTimeout(() => {

        typingDiv.remove();   // remove typing

        addMessage("bot", data.response);

        chatHistory.push({
            type: "bot",
            message: data.response
        });

        saveChat();

    }, 1200);
}




function quickSend(text) {
    document.getElementById("message").value = text;
    sendMessage();
}


window.onload = function () {

    let chatArea = document.getElementById("chat-area");

    let stored = localStorage.getItem("chatHistory");

    if (stored) {
        chatHistory = JSON.parse(stored);

        chatHistory.forEach(chat => {
            if (chat.type === "user") {
                chatArea.innerHTML +=
                    `<div class="user-msg">${chat.message}</div>`;
            } else {
                chatArea.innerHTML +=
                    `<div class="bot-msg">${chat.message}</div>`;
            }
        });

    } else {

        chatArea.innerHTML += `
            <div class="bot-msg">
                Hello! I'm Manoj's portfolio assistant.<br><br>
                You can ask me about:
                <br><br>

                <div class="suggestions">
                    <button onclick="quickSend('about')">About</button>
                    <button onclick="quickSend('skills')">Skills</button>
                    <button onclick="quickSend('projects')">Projects</button>
                    <button onclick="quickSend('experience')">Experience</button>
                    <button onclick="quickSend('contact')">Contact</button>
                </div>
            </div>
        `;
    }

    document.getElementById("message").focus();
};


function saveChat() {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
}



function clearChat() {

    localStorage.removeItem("chatHistory");
    chatHistory = [];

    let chatArea = document.getElementById("chat-area");
    chatArea.innerHTML = "";

    // show welcome message again
    chatArea.innerHTML += `
        <div class="bot-msg">
            Hello! I'm Manoj's portfolio assistant.<br><br>
            You can ask me about:
            <br><br>

            <div class="suggestions">
                <button onclick="quickSend('about')">About</button>
                <button onclick="quickSend('skills')">Skills</button>
                <button onclick="quickSend('projects')">Projects</button>
                <button onclick="quickSend('experience')">Experience</button>
                <button onclick="quickSend('contact')">Contact</button>
            </div>
        </div>
    `;
}


function addMessage(type, content) {

    let chatArea = document.getElementById("chat-area");

    let div = document.createElement("div");
    div.className = type === "user" ? "user-msg" : "bot-msg";
    div.innerHTML = content;

    chatArea.appendChild(div);

    chatArea.scrollTo({
        top: chatArea.scrollHeight,
        behavior: "smooth"
    });
}
