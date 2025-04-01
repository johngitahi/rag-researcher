import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function ChatUploadApp() {
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first");
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });
    setLoading(false);
    const data = await response.json();
    alert(data.message || "File uploaded successfully");
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setInput("");

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      setMessages((prev) => {
        const updatedMessages = [...prev];
        updatedMessages[updatedMessages.length - 1].content += decoder.decode(value);
        return updatedMessages;
      });
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-4">
      <div className="border p-4 rounded-lg">
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <button onClick={handleUpload} disabled={loading} className="ml-2 bg-blue-500 text-white px-4 py-2 rounded">
          {loading ? "Uploading..." : "Upload"}
        </button>
      </div>

      <div className="border p-4 rounded-lg h-96 overflow-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`my-2 p-2 rounded ${msg.role === "user" ? "bg-gray-200" : "bg-green-200"}`}>
            <strong>{msg.role === "user" ? "You:" : "Assistant:"}</strong>
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
      </div>

      <div className="flex items-center border p-2 rounded-lg">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          className="flex-1 border-none outline-none p-2"
        />
        <button onClick={handleSendMessage} className="ml-2 bg-blue-500 text-white px-4 py-2 rounded">
          Send
        </button>
      </div>
    </div>
  );
}

