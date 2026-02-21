import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi, I am Surendar Ram's AI assistant. Ask anything about Surendar.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question: input,
      });

      const botMessage = { sender: "bot", text: response.data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Something went wrong." },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          Surendar Ram's AI Assistant
        </div>

        <div className="chat-body">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              {msg.text}
            </div>
          ))}
          {loading && <div className="message bot">Typing...</div>}
        </div>

        <div className="chat-footer">
          <input
            type="text"
            placeholder="Ask something about Surendar..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;