class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }

        let req = new XMLHttpRequest();
        req.open("GET", "http://127.0.0.1:5000/predict/"+text1)
        req.send()
        req.onload = () => {
            let msg2 = { name: "Charlie", message: JSON.parse(req.response) };
            this.messages.push(msg1);
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''
            console.log(msg2)
        }
    }

    updateChatText(chatbox) {
        var html = '';
        var prev = '';
        var usr = '';
        this.messages.slice().forEach(function(item, index) {
            console.log(item.name)
            if (item.name === "User")
            {
                usr = '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                html = '<div class="messages__item messages__item--operator">' + item.message + '</div>' + prev
                const chatmessage = chatbox.querySelector('.chatbox__messages');
                chatmessage.innerHTML = html;
            }
            else
            {
                prev = '<div class="messages__item messages__item--visitor">' + item.message + '</div>' + usr + prev
                html = prev
                setTimeout(function() {
                    const chatmessage = chatbox.querySelector('.chatbox__messages');
                    chatmessage.innerHTML = html;
                  }, 1000);
            }
          });
    }
}


const chatbox = new Chatbox();
chatbox.display();