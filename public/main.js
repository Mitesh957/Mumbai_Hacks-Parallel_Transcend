const socket = io();

const clientsTotal = document.getElementById('client-total');
const messageContainer = document.getElementById('message-container');
const nameInput = document.getElementById('name-input');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const fileInput = document.getElementById('file-input');

const messageTone = new Audio('/message-tone.mp3');

let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

function loadChatHistory() {
  chatHistory.forEach(data => {
    addMessageToUI(data.isOwnMessage, data);
  });
}

loadChatHistory();

messageForm.addEventListener('submit', (e) => {
  e.preventDefault();
  sendMessage();
});

fileInput.addEventListener('change', handleFileSelect);

socket.on('clients-total', (data) => {
  clientsTotal.innerText = `Total Clients: ${data}`;
});

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  if (!validateFile(file)) {
    fileInput.value = '';
    return;
  }

  messageInput.placeholder = `Loading ${file.name}...`;
  messageInput.disabled = true;

  const reader = new FileReader();
  reader.onload = function(e) {
    const fileData = {
      name: file.name,
      type: file.type,
      data: e.target.result
    };

    messageInput.placeholder = "Type your message...";
    messageInput.disabled = false;

    sendMessage(fileData);
  };

  reader.onerror = function() {
    messageInput.placeholder = "Error loading file. Please try again.";
    messageInput.disabled = false;
    setTimeout(() => {
      messageInput.placeholder = "Type your message...";
    }, 2000);
  };

  if (file.type.startsWith('image/') || file.type === 'application/pdf') {
    reader.readAsDataURL(file);
  }
}

function validateFile(file) {
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    alert('File is too large. Please choose a file under 5MB.');
    return false;
  }
  return true;
}

function sendMessage(fileData = null) {
  if (messageInput.value === '' && !fileData) return;

  const data = {
    name: nameInput.value,
    message: messageInput.value,
    dateTime: new Date(),
    file: fileData
  };

  socket.emit('message', data);
  addMessageToUI(true, data);
  
  chatHistory.push({...data, isOwnMessage: true});
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  
  messageInput.value = '';
  fileInput.value = '';
}

socket.on('chat-message', (data) => {
  messageTone.play().catch(error => console.error('Error playing message tone:', error));
  addMessageToUI(false, data);
  
  chatHistory.push({...data, isOwnMessage: false});
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
});

function addMessageToUI(isOwnMessage, data) {
  clearFeedback();
  
  let fileElement = '';
  if (data.file) {
    if (data.file.type.startsWith('image/')) {
      fileElement = `
        <div class="message-attachment">
          <img src="${data.file.data}" alt="Shared image">
        </div>`;
    } else if (data.file.type === 'application/pdf') {
      const blob = dataURItoBlob(data.file.data);
      const url = URL.createObjectURL(blob);
      
      fileElement = `
        <div class="message-attachment">
          <embed src="${url}" type="application/pdf" width="100%" height="300px" />
        </div>`;
    }
  }

  const element = `
    <li class="${isOwnMessage ? 'message-right' : 'message-left'}">
      <p class="message">
        ${data.message ? `<span class="message-text">${data.message}</span>` : ''}
        ${fileElement}
        <span class="message-info">${data.name} ● ${moment(data.dateTime).fromNow()}</span>
      </p>
    </li>
  `;
  
  messageContainer.innerHTML += element;
  scrollToBottom();
}

function dataURItoBlob(dataURI) {
  const byteString = atob(dataURI.split(',')[1]);
  const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], {type: mimeString});
}

function scrollToBottom() {
  messageContainer.scrollTo(0, messageContainer.scrollHeight);
}

messageInput.addEventListener('focus', (e) => {
  socket.emit('feedback', {
    feedback: `✍️ ${nameInput.value} is typing a message`,
  });
});

messageInput.addEventListener('keypress', (e) => {
  socket.emit('feedback', {
    feedback: `✍️ ${nameInput.value} is typing a message`,
  });
});

messageInput.addEventListener('blur', (e) => {
  socket.emit('feedback', {
    feedback: '',
  });
});

socket.on('feedback', (data) => {
  clearFeedback();
  const element = `
    <li class="message-feedback">
      <p class="feedback" id="feedback">${data.feedback}</p>
    </li>
  `;
  messageContainer.innerHTML += element;
});

function clearFeedback() {
  document.querySelectorAll('li.message-feedback').forEach((element) => {
    element.parentNode.removeChild(element);
  });
}

// Clean up Blob URLs when the window is closed
window.addEventListener('beforeunload', () => {
  const embeds = document.querySelectorAll('embed[src^="blob:"]');
  embeds.forEach(embed => {
    URL.revokeObjectURL(embed.src);
  });
});