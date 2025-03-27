const sidebar = document.querySelector("#sidebar");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");

hide_sidebar.addEventListener( "click", function() {
    sidebar.classList.toggle( "hidden" );
} );

const user_menu = document.querySelector(".user-menu ul");
const show_user_menu = document.querySelector(".user-menu button");

show_user_menu.addEventListener( "click", function() {
    if( user_menu.classList.contains("show") ) {
        user_menu.classList.toggle( "show" );
        setTimeout( function() {
            user_menu.classList.toggle( "show-animate" );
        }, 200 );
    } else {
        user_menu.classList.toggle( "show-animate" );
        setTimeout( function() {
            user_menu.classList.toggle( "show" );
        }, 50 );
    }
} );

const models = document.querySelectorAll(".model-selector button");

for( const model of models ) {
    model.addEventListener("click", function() {
        document.querySelector(".model-selector button.selected")?.classList.remove("selected");
        model.classList.add("selected");
    });
}

const message_box = document.querySelector("#message");

message_box.addEventListener("keyup", function() {
    message_box.style.height = "auto";
    let height = message_box.scrollHeight + 2;
    if( height > 200 ) {
        height = 200;
    }
    message_box.style.height = height + "px";
});

function show_view( view_selector ) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

new_chat_button.addEventListener("click", function() {
    show_view( ".new-chat-view" );
});

document.querySelectorAll(".conversation-button").forEach(button => {
    button.addEventListener("click", function() {
        show_view( ".conversation-view" );
    })
});







// Replace with your WebSocket endpoint (adjust protocol if using HTTPS)
const socket = new WebSocket('ws://localhost:8000/ws/conversation/Kd2ayrDx6fzvyU3nyBpKk6/');

// Ensure binary messages are received as ArrayBuffer
socket.binaryType = "arraybuffer";

// Listen for connection open
socket.addEventListener('open', () => {
  console.log('WebSocket connection opened.');
});

// Listen for incoming messages
socket.addEventListener('message', (event) => {
  // Check if event.data is a string (text message) or binary (audio chunk)
  if (typeof event.data === 'string') {
    try {
      const data = JSON.parse(event.data);
      
      // Handle partial transcription updates
      if (data.type && data.type === "partial") {
        updatePartialMessage(data.text);
      
      // Handle full text messages from the assistant or user
      } else if (data.message && data.message_type && data.sender) {
        // Remove any existing partial transcription UI
        removePartialMessage();
        displayMessage(data);
      }
    } catch (e) {
      console.error("Error parsing JSON:", e);
    }
  } else {
    // Assume binary data is an audio chunk and handle accordingly
    handleAudioChunk(event.data);
  }
});

// Function to update partial transcription feedback in the UI
function updatePartialMessage(text) {
  let partialEl = document.getElementById('partial-message');
  if (!partialEl) {
    partialEl = document.createElement('div');
    partialEl.id = 'partial-message';
    // Use assistant styling for partial results
    partialEl.className = 'assistant message partial';
    partialEl.innerHTML = `
      <div class="identity"><i class="gpt user-icon">AI</i> chatAI</div>
      <div class="content"><p>${text}</p></div>
    `;
    document.querySelector('.conversation-view').appendChild(partialEl);
  } else {
    partialEl.querySelector('.content p').textContent = text;
  }
}

// Remove the partial transcription element when a full message is ready
function removePartialMessage() {
  const partialEl = document.getElementById('partial-message');
  if (partialEl) {
    partialEl.remove();
  }
}

// Function to handle and play incoming audio chunks
function handleAudioChunk(data) {
  // Create a Blob from the binary data; adjust the MIME type if needed
  const blob = new Blob([data], { type: 'audio/webm' });
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);
  audio.play();
}

// Function to display text messages in the conversation view
function displayMessage(messageData) {
  const sender = messageData.sender.toLowerCase();
  const messageEl = document.createElement('div');
  
  // Set the message element class based on the sender
  if (sender === 'samuelobinnachimdi') {
    messageEl.className = 'user message';
  } else if (sender === 'ai_assistant' || sender === 'chatai') {
    messageEl.className = 'assistant message';
  } else {
    messageEl.className = 'message';
  }
  
  // Create the identity element with a label specific to the sender
  const identityEl = document.createElement('div');
  identityEl.className = 'identity';
  if (sender === 'samuelobinnachimdi') {
    identityEl.innerHTML = '<i class="user-icon">U</i> samuelobinnachimdi';
  } else if (sender === 'ai_assistant' || sender === 'chatai') {
    identityEl.innerHTML = '<i class="gpt user-icon">AI</i>';
  } else {
    identityEl.innerHTML = `<i class="user-icon">?</i>`;
  }
  
  // Create the content element with the message text
  const contentEl = document.createElement('div');
  contentEl.className = 'content';
  contentEl.innerHTML = `<p>${messageData.message}</p>`;
  
  // Append identity and content to the message element
  messageEl.appendChild(identityEl);
  messageEl.appendChild(contentEl);
  
  // Append the message to the conversation view and scroll to the bottom
  const conversationView = document.querySelector('.conversation-view');
  conversationView.appendChild(messageEl);
  conversationView.scrollTop = conversationView.scrollHeight;
}

// Send message when the send button is clicked
document.querySelector('.send-button').addEventListener('click', sendMessage);

// Also send message on pressing the Enter key (without shift) in the textarea
document.getElementById('message').addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

// Function to send a text message to the backend
function sendMessage() {
  const messageInput = document.getElementById('message');
  const messageText = messageInput.value.trim();
  if (messageText === '') return; // Prevent sending empty messages

  // Create the message object to match your backend expectations
  const messageData = {
    message: messageText,
    message_type: "text_message",
    sender: "samuelobinnachimdi"
  };

  // Send the JSON string over the WebSocket
  socket.send(JSON.stringify(messageData));
  
  // Display the user message immediately in the conversation view
  displayMessage(messageData);

  // Clear the textarea
  messageInput.value = '';
}
