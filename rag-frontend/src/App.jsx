import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = { type: "user", content: input };
    setMessages([...messages, userMessage]);

    // Clear input and set loading
    setInput("");
    setLoading(true);

    try {
      // Call backend API
      const response = await axios.post("http://localhost:8000/ask", {
        query: input,
        top_k: 3,
      });

      // Add bot response to chat
      const botMessage = {
        type: "bot",
        content: response.data.answer,
        sources: response.data.sources,
      };

      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      // Add error message
      const errorMessage = {
        type: "bot",
        content: "Sorry, I encountered an error processing your request.",
        error: true,
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>MAth Pro FAQ Chatbot</h1>
      </header>

      <div className="chat-container">
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              Ask a question about your PDF document!
            </div>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`message ${message.type}`}>
                <div className="message-content">{message.content}</div>
                {message.sources && (
                  <div className="sources">
                    <details>
                      <summary>Sources</summary>
                      <ul>
                        {message.sources.map((source, idx) => (
                          <li key={idx}>{source}</li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <div className="message bot loading">
              <div className="loading-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
