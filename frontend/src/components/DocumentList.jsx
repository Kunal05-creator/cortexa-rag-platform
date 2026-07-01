import { useEffect, useState } from "react";
import API from "../services/api";

function DocumentsList() {
  const [documents, setDocuments] = useState([]);
  const [count, setCount] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const res = await API.get("/documents");
      setDocuments(res.data.documents || []);
      setCount(res.data.count || 0);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteDocument = async (filename) => {
    if (!window.confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }
    try {
      await API.delete(`/documents/${filename}`);
      await loadDocuments(); // refresh list
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to delete document. Please try again.");
    }
  };

  const filtered = documents.filter((doc) =>
    doc.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="mt-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-purple-400 font-bold">Documents</h3>
        <span className="text-xs bg-slate-800 px-2 py-1 rounded-lg">{count}</span>
      </div>

      <input
        type="text"
        placeholder="Search documents..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 mb-4 outline-none focus:border-purple-500 text-sm"
      />

      <button
        onClick={loadDocuments}
        className="w-full mb-4 bg-slate-800 hover:bg-slate-700 rounded-xl py-2 transition"
      >
        Refresh
      </button>

      <div className="space-y-3 max-h-[420px] overflow-y-auto">
        {loading && <div className="text-center text-slate-400">Loading...</div>}

        {!loading && filtered.length === 0 && (
          <div className="bg-slate-900 rounded-xl p-4 text-center text-slate-400">
            No documents found.
          </div>
        )}

        {filtered.map((doc, index) => (
          <div
            key={index}
            className="bg-slate-800 hover:bg-slate-700 transition rounded-xl p-4 border border-slate-700"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="font-medium truncate">📄 {doc.name}</div>
                <div className="text-xs text-slate-400 mt-1">{doc.size_mb} MB</div>
              </div>
              <button
                onClick={() => deleteDocument(doc.name)}
                className="text-red-400 hover:text-red-300 text-lg"
                title="Delete document"
              >
                🗑
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DocumentsList;