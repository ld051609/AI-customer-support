'use client'
import React, { useState } from 'react';
import './Chatbot.css'; // Import the CSS file

const page = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async () => {
    setIsStreaming(true);
    const response = await fetch('http://127.0.0.1:5000', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    });
    const data = await response.json();
    setMessages([...messages, data.message]);
    setInput('');
    setIsStreaming(false);
  };

  return (
    <div className='main-container'>
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className="chat-message">
            {msg}
          </div>
        ))}
      </div>
      <div className="chat-input-container">
        <input
          type='text'
          value={input}
          onChange={e => setInput(e.target.value)}
          className="chat-input"
          disabled={isStreaming}
          />
        <button
          onClick={sendMessage}
          disabled={isStreaming}
          className="chat-button"
          >
          {isStreaming ? 'Waiting...' : 'Send'}
        </button>
      </div>
    </div>
  </div>
  );
};

export default page;
