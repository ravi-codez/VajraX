import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Upload PDF
  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("http://127.0.0.1:8000/upload-pdf", {
        method: "POST",
        body: formData,
      });

      alert("PDF uploaded and processed successfully");
    } catch (error) {
      alert("Failed to upload PDF");
    }
  };

  // Send chat message
  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to history
    const userMessage = { role: "user", content: input };
    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: input,
          history: updatedMessages, // 👈 send full conversation
        }),
      });

      const data = await response.json();

      const assistantMessage = {
        role: "assistant",
        content: data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error fetching response." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <div className="header">
        <h2>Chat with your PDF</h2>
        <div className="upload-box">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={uploadPDF}>Upload PDF</button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="chat-container">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${
              msg.role === "user" ? "user" : "assistant"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="chat-message assistant">Typing...</div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Box */}
      <div className="input-container">
        <input
          type="text"
          placeholder="Ask a question about your PDF..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
