'use client'
import React, { useState } from 'react';
import './Chatbot.css'; // Import the CSS file

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async () => {
    setIsStreaming(true);

    try {
      const response = await fetch('http://127.0.0.1:5000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages([...messages, { text: input, type: 'user' }, { text: data.response, type: 'bot' }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages([...messages, { text: input, type: 'user' }, { text: 'Sorry, something went wrong.', type: 'bot' }]);
    }

    setInput('');
    setIsStreaming(false);
  };

  return (
    <div className='main-container'>
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.type}`}>
              <p>{msg.text}</p>
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

export default Chatbot;
