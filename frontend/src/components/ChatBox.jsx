import { useState } from "react";
import API from "../services/api";

function ChatBox({ uploaded }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);

      const res = await API.post("/ask", {
        question,
      });

      setAnswer(res.data.answer);
      setSources(res.data.sources || []);

    } catch (error) {
      console.error(error);
      setAnswer("Error getting response");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 min-h-[600px]">

      <h2 className="text-2xl font-bold mb-4 text-black">
        💬 Ask Cortexa
      </h2>

      {!uploaded && (
        <div className="bg-yellow-100 border border-yellow-300 text-yellow-800 p-4 rounded-lg mb-4">
          Upload a PDF first to start asking questions.
        </div>
      )}

      <div className="flex gap-3">

        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about your document..."
          className="flex-1 border rounded-lg p-3"
        />

        <button
          onClick={askQuestion}
          disabled={!uploaded || loading}
          className="bg-black text-white px-6 rounded-lg hover:bg-gray-800 transition"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

      </div>

      {answer && (
        <div className="mt-8">

          <h3 className="font-bold text-lg mb-3 text-black">
            Answer
          </h3>

          <div className="bg-gray-100 p-4 rounded-xl whitespace-pre-wrap">
            {answer}
          </div>

          <h3 className="font-bold text-lg mt-6 mb-3 text-black">
            Sources
          </h3>

          <div className="space-y-3">

            {sources.map((source, index) => (
              <div
                key={index}
                className="border rounded-xl p-3 bg-gray-50"
              >
                <div className="font-medium">
                  📄 {source.source.split("/").pop()}
                </div>

                <div className="text-sm text-gray-600">
                  Page {source.page}
                </div>
              </div>
            ))}

          </div>

        </div>
      )}

    </div>
  );
}

export default ChatBox;