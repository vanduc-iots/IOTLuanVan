const checkElement = document.getElementById("check-5");
document.getElementById("check-5").addEventListener("change", () => {
    let theme = (checkElement.checked) ? "light" : "dark";
    document.querySelector("[data-bs-theme]").setAttribute("data-bs-theme", theme);
    localStorage.setItem('theme', theme)
});

document.addEventListener("DOMContentLoaded", () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.querySelector("[data-bs-theme]")
            .setAttribute('data-bs-theme', currentTheme);
        if (currentTheme == "dark") checkElement.checked = false;
        else checkElement.checked = true;
    } else {
        document.querySelector("[data-bs-theme]")
            .setAttribute('data-bs-theme', "light");
    }
});

const prompt = document.getElementById("prompt-text");

function submitVoiceMessage() {
    const message = prompt.value.trim();
    console.log('[voice] submitVoiceMessage called. message=', message);
    if (!message) return;

    let userAttachment = filesChoosen[0];
    appendMessageBox(message, "user", userAttachment);
    closeFileChoosen();
    try {
        if (userAttachment) {
            if (userAttachment.startsWith("data:"))
                userAttachment = userAttachment.split(",")[1];
            sendMessageReq(message, userAttachment);
        } else {
            sendMessageReq(message);
        }
    } catch (err) {
        console.error('[voice] sendMessageReq failed', err);
    }

    // fallback: ensure the form submit/button click happens if direct call doesn't work
    setTimeout(() => {
        const sendBtn = document.getElementById('send-message');
        if (sendBtn) {
            console.log('[voice] fallback: clicking send button');
            sendBtn.click();
        }
    }, 150);

    prompt.value = "";
    sendMessageBtn.classList.remove("show-send-btn");
}

document.getElementById("form").addEventListener("submit", (e) => {
    e.preventDefault();
    submitVoiceMessage();
});

const sendMessageBtn = document.getElementById("form");
prompt.addEventListener("keydown", (evt) => {
    if ((evt.key === "Enter" || evt.keyCode === 13) && !evt.shiftKey) {
        evt.preventDefault();
        document.getElementById("send-message").click();
    }
});

prompt.addEventListener("input", (evt) => { // Bắt sự kiện nhập phím
    if (evt.target.value == "")
        sendMessageBtn.classList.remove("show-send-btn");
    else
        sendMessageBtn.classList.add("show-send-btn");
});

prompt.addEventListener("paste", function (e) {

});

const copyBtns = document.querySelectorAll("#copy-code").forEach(btn => {
    btn.addEventListener("click", function () {
        console.log(this);

        const preElement = this.parentElement.parentElement.parentElement;
        const code_string = preElement.children.item(1).textContent;
        navigator.clipboard.writeText(code_string)
            .then(() => console.log('Text copied!'))
            .catch(() => console.log("copy faild"))
    });
});

function addImageEvent(img) {
    img.addEventListener("click", () => {
        document.querySelector(".image-modal").setAttribute("src", img.src);
        document.querySelector('button[data-bs-toggle="modal"]').click();
    });
}

function appendMessageBox(message, objectName = "user", imageBase64 = null) {
    const divBox = document.createElement("div");
    const chatbox = document.getElementById("chat-box");
    divBox.className = `${objectName}-box`;
    if (objectName == "user") {
        if (imageBase64) {
            const spanImgElement = document.createElement('span');
            spanImgElement.setAttribute("style", `background: url("${imageBase64}") 50% center / cover;`)
            spanImgElement.className = "image mb-1";
            spanImgElement.addEventListener("click", (e) => {
                console.log(e.target);
            });
            divBox.appendChild(spanImgElement);
        }
        divBox.innerHTML += `<p class="p-3 text-tertiary" id="user-message">
            <span>${message}</span></p>`;
    }
    else {
        // trường hợp là model
        divBox.id = "bot-message";
        divBox.innerHTML = marked.parse(message);
        if (divBox.querySelector("p>img")) {
            const imgEle = divBox.querySelector("p>img");
            imgEle.id = "bot-attchment";
            addImageEvent(imgEle);
        }
    }
    chatbox.appendChild(divBox);
    window.scrollTo(0, document.body.scrollHeight);
    return divBox;
}

function addToolBarCodeBox(title, element) {
    element.innerHTML += `<nav class="navbar"> 
            <div class="container"> <span>${title}</span>
            <button class="btn" aria-label="Copy" id="copy-code">
            <span><i class="bi bi-copy"></i></span></button></div></nav>`;
    element.insertBefore(element.lastChild, element.firstChild);
    const copy_btn = element.querySelector("#copy-code");
    copy_btn.addEventListener("click", () => {
        navigator.clipboard.writeText(element.lastChild.textContent)
            .then(() => {
                const copyIcon = copy_btn.cloneNode(true).innerHTML;
                const copySuccess_btn = '<span><i class="bi bi-check-lg"></i></span>';
                copy_btn.innerHTML = copySuccess_btn;
                setTimeout(() => copy_btn.innerHTML = copyIcon, 2000);
            });
    });
}

function selectPreElement(parentElement) {
    Array.from(parentElement.children).forEach((item) => {
        if (item.tagName == "PRE") {
            const firstChild = item.firstChild;
            if (firstChild?.tagName == "CODE") {
                console.log(firstChild.className);
                let language = firstChild.className.match(/language-[\w#.+]+/)[0].slice(9);
                language = (language == "undefined") ? "Kết quả" : language;
                addToolBarCodeBox(language, item);
            }
        }
        if (item.tagName == "UL" || item.tagName == "LI")
            selectPreElement(item);
    });
}

function botWriteText(textToWrite) {
    const divBotBox = appendMessageBox(textToWrite, "model");
    hljs.highlightAll();
    selectPreElement(divBotBox);
    Array.from(divBotBox.children).forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('visible');
        }, index * 100);
    });
}

function sendMessageReq(userMessage, userAttachment) {
    fetch("/bot", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage, attchment: userAttachment })
    }).then(res => { if (res.ok) return res.json() })
        .then(data => {
            if (data.model) {
                let model_message = data.model.message;
                if (data.model.image)
                    model_message += "\n\n" + `![](${data.model.image})`;

                botWriteText(model_message);
                window.scrollTo(0, document.body.scrollHeight);
            }
        });
}


const mime_file_allow = [
    "application/pdf",
    "image/*",
    "application/x-javascript",
    "text/javascript",
    "video/mp4",
    "application/x-python",
    "text/x-python",
    "text/css",
    "text/csv",
    "text/html",
    "text/plain",
    "text/md"
]
const filesChoosen = []
function fileChooser() {
    const inputFile = document.createElement("input");
    inputFile.type = "file"
    inputFile.accept = mime_file_allow.toString();
    inputFile.click();
    inputFile.onchange = (e) => {
        const file_choosen = e.target.files[0];
        const fileReader = new FileReader();
        fileReader.onload = (readerEvt) => {
            const fileBase64 = readerEvt.target.result;
            const userFileWriter = document.querySelector(".userAttchment>span");
            if (!file_choosen.type.startsWith("image")) { // nếu có kiểu là image
                const mimeType = file_choosen.type;
                const fileType = mimeType.slice(mimeType.indexOf("/") + 1);
                userFileWriter.style.backgroundImage = `url(/static/images/icons/${fileType}-file-icon.png)`;
            } else { // kiểu file
                userFileWriter.style.backgroundImage = `url(${fileBase64})`;
            }
            filesChoosen.pop(); // tạm thời cho xóa r thay ảnh khác
            filesChoosen.push(fileBase64); //add
            userFileWriter.getElementsByTagName("button").item(0)
                .onclick = (e) => closeFileChoosen(e.target)
            userFileWriter.parentElement.classList.remove("d-none");
        }
        fileReader.readAsDataURL(file_choosen, 'UTF-8');
    };
}

function closeFileChoosen(element = null) {
    filesChoosen.length = 0 // clear cái mảng file
    if (element) {
        element.parentElement.style.backgroundImage = ""
        document.querySelector(".userAttchment").classList.add('d-none');
    } else {
        closeFileChoosen(document.querySelector(".userAttchment>span>button"));
    }
}

// ==================== VOICE RECOGNITION ====================
const voiceBtn = document.getElementById("voice-btn");
const voiceIcon = document.getElementById("voice-icon");
const voiceText = document.getElementById("voice-text");
let voiceAutoSubmitting = false;

if (voiceBtn && voiceRecognition.isSupported) {
    voiceBtn.addEventListener("click", (e) => {
        e.preventDefault();
        
        if (voiceRecognition.isListening) {
            // Stop recording manually if user clicks again
            const transcript = voiceRecognition.stop();
            updateVoiceBtnUI(false);
            
            if (transcript && !voiceAutoSubmitting) {
                prompt.value = transcript;
                voiceAutoSubmitting = true;
                setTimeout(() => submitVoiceMessage(), 200);
            }
        } else {
            // Start recording
            voiceAutoSubmitting = false;
            voiceRecognition.start();
            updateVoiceBtnUI(true);
        }
    });
    
    // Handle voice recognition callbacks
    voiceRecognition.onStart = () => {
        console.log('Voice recognition started');
        voiceAutoSubmitting = false;
        updateVoiceBtnUI(true);
    };
    
    voiceRecognition.onResult = (result) => {
        // Update prompt text with interim results
        if (result.final) {
            prompt.value = result.final;
        } else {
            prompt.value = result.final || result.interim;
        }
        
        if (prompt.value) {
            sendMessageBtn.classList.add("show-send-btn");
        }

        if (result.isFinal && prompt.value && !voiceAutoSubmitting) {
            voiceAutoSubmitting = true;
            setTimeout(() => submitVoiceMessage(), 200);
        }
    };
    
    voiceRecognition.onEnd = () => {
        console.log('Voice recognition ended');
        updateVoiceBtnUI(false);

        if (prompt.value && !voiceAutoSubmitting) {
            voiceAutoSubmitting = true;
            setTimeout(() => submitVoiceMessage(), 200);
        }
    };
    
    voiceRecognition.onError = (error) => {
        console.error('Voice recognition error:', error);
        updateVoiceBtnUI(false);
        
        // Show notification to user
        showVoiceNotification(error.message, 'error');
    };
    
    function updateVoiceBtnUI(isListening) {
        if (isListening) {
            voiceIcon.className = 'bi bi-mic-fill';
            voiceText.textContent = 'Đang lắng nghe...';
            voiceBtn.classList.add('listening');
        } else {
            voiceIcon.className = 'bi bi-mic';
            voiceText.textContent = 'Ghi âm';
            voiceBtn.classList.remove('listening');
        }
    }
    
    function showVoiceNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : 'info'} position-fixed top-0 start-50 translate-middle-x mt-3`;
        notification.style.zIndex = '9999';
        notification.style.maxWidth = '400px';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade');
            setTimeout(() => notification.remove(), 150);
        }, 3000);
    }
} else if (voiceBtn && !voiceRecognition.isSupported) {
    voiceBtn.disabled = true;
    voiceBtn.title = 'Web Speech API không được hỗ trợ trên trình duyệt này';
    voiceText.textContent = 'Không hỗ trợ';
}
