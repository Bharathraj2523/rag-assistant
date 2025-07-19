// Chat logic for chat.html

document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    // Helper to render a single message
    function renderMessage(message) {
        const div = document.createElement('div');
        div.classList.add('message', message.role);
        div.textContent = message.content;
        chatWindow.appendChild(div);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Render all messages
    function renderHistory(history) {
        chatWindow.innerHTML = '';
        history.forEach(renderMessage);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Load chat history on page load
    fetch('/chat_api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: '' }) // Empty message to just get history
    })
    .then(res => res.json())
    .then(data => {
        if (data.history) {
            renderHistory(data.history);
        }
    });

    // Handle form submit
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userMsg = chatInput.value.trim();
        if (!userMsg) return;

        // Optimistically render user message
        renderMessage({ role: 'user', content: userMsg });
        chatInput.value = '';
        chatInput.focus();

        fetch('/chat_api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMsg })
        })
        .then(res => res.json())
        .then(data => {
            if (data.history) {
                // Only render the last assistant message
                const lastMsg = data.history[data.history.length - 1];
                if (lastMsg && lastMsg.role === 'assistant') {
                    renderMessage(lastMsg);
                }
            }
        });
    });
});
