import { useState } from "react";
import API from "../services/api";

function ChatBox({ uploaded }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    const currentQuestion = question;
    setMessages((prev) => [...prev, { type: "user", content: currentQuestion }]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await API.post("/ask", { question: currentQuestion });
      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          content: res.data.answer,
          sources: res.data.sources || [],
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { type: "ai", content: "Error getting response.", sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0f172a] rounded-2xl shadow-xl p-6 h-[700px] flex flex-col">
      <h2 className="text-2xl font-bold text-purple-400 mb-4">Cortexa Assistant</h2>

      {!uploaded && (
        <div className="bg-yellow-500/20 border border-yellow-500 text-yellow-300 p-3 rounded-lg mb-4">
          Upload documents first.
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, index) => (
          <div key={index}>
            {msg.type === "user" ? (
              <div className="flex justify-end">
                <div className="bg-purple-600 text-white px-4 py-3 rounded-2xl max-w-[80%]">
                  {msg.content}
                </div>
              </div>
            ) : (
              <div className="flex justify-start">
                <div className="bg-slate-800 text-white px-4 py-3 rounded-2xl max-w-[80%]">
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                  {msg.sources?.length > 0 && (
                    <div className="mt-4 border-t border-slate-700 pt-3">
                      <p className="text-xs text-purple-300 mb-2">Sources</p>
                      {msg.sources.map((source, i) => (
                        <div key={i} className="text-xs text-slate-300">
                          {source.source.split("/").pop()} • Page {source.page}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-slate-300 px-4 py-3 rounded-2xl">
              Analyzing documents...
            </div>
          </div>
        )}
      </div>

      <div className="mt-4 flex gap-3">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          placeholder="Ask anything about your documents..."
          className="flex-1 bg-slate-800 text-white border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-purple-500"
        />
        <button
          onClick={askQuestion}
          disabled={!uploaded || loading}
          className="bg-purple-600 hover:bg-purple-700 text-white px-6 rounded-xl transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatBox;