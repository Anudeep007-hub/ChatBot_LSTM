import React from 'react';
import '../styles/userpage.css'; // Assuming styles are defined here

function ChatMessage({ sender, text }) {
    return (
        <div className={`message ${sender === 'bot' ? 'bot-message' : 'user-message'}`}>
            {text}
        </div>
    );
}

export default ChatMessage;
