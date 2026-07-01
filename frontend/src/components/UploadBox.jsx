import { useState } from "react";
import API from "../services/api";
import DocumentsList from "./DocumentList";

function UploadBox({ setUploaded }) {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadPDF = async () => {
    if (files.length === 0) {
      setStatus("Please select one or more PDFs.");
      return;
    }

    const formData = new FormData();
    files.forEach((pdf) => {
      formData.append("files", pdf);
    });

    try {
      setLoading(true);
      setStatus(`Uploading ${files.length} document(s)...`);
      const res = await API.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(res.data.message);
      setUploaded(true);
      setFiles([]);
    } catch (err) {
      console.error(err);
      setStatus("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0f172a] rounded-2xl shadow-xl p-6 h-full overflow-y-auto">
      <h2 className="text-2xl font-bold text-purple-400">Knowledge Base</h2>
      <p className="text-slate-400 text-sm mt-2 mb-6">
        Upload one or multiple PDF documents.
      </p>

      <label
        htmlFor="pdf-upload"
        className="flex flex-col items-center justify-center border-2 border-dashed border-purple-500 rounded-2xl p-8 cursor-pointer hover:bg-slate-800 transition"
      >
        <div className="text-5xl mb-4">📄</div>
        <p className="font-semibold">Drag & Drop PDFs</p>
        <p className="text-slate-400 text-sm mt-1">or click to browse</p>
      </label>

      <input
        id="pdf-upload"
        type="file"
        multiple
        accept=".pdf"
        className="hidden"
        onChange={(e) => setFiles([...e.target.files])}
      />

      {files.length > 0 && (
        <div className="mt-5">
          <h3 className="text-sm text-slate-400 mb-3">Selected Files</h3>
          <div className="space-y-3">
            {files.map((pdf, index) => (
              <div key={index} className="bg-slate-800 rounded-xl p-3">
                <div className="flex justify-between">
                  <p className="truncate font-medium">{pdf.name}</p>
                  <button
                    onClick={() => setFiles(files.filter((_, i) => i !== index))}
                    className="text-red-400 hover:text-red-300"
                  >
                    ✕
                  </button>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  {(pdf.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={uploadPDF}
        disabled={loading || files.length === 0}
        className={`w-full mt-6 py-3 rounded-xl font-semibold transition ${
          loading || files.length === 0
            ? "bg-slate-700 cursor-not-allowed"
            : "bg-purple-600 hover:bg-purple-700"
        }`}
      >
        {loading
          ? `Indexing ${files.length} document(s)...`
          : `Upload & Index ${files.length > 0 ? `(${files.length})` : ""}`}
      </button>

      {loading && (
        <div className="mt-4">
          <div className="w-full bg-slate-800 rounded-full h-2">
            <div className="bg-purple-500 h-2 rounded-full animate-pulse w-full"></div>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            Creating embeddings and indexing documents...
          </p>
        </div>
      )}

      {status && (
        <div
          className={`mt-5 rounded-xl p-4 text-sm ${
            status.toLowerCase().includes("failed")
              ? "bg-red-900/30 text-red-300 border border-red-700"
              : "bg-green-900/20 text-green-300 border border-green-700"
          }`}
        >
          {status}
        </div>
      )}

      <div className="mt-8">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-purple-300">Indexed Documents</h3>
          <button
            onClick={() => window.location.reload()}
            className="text-xs text-purple-400 hover:text-purple-300"
          >
            Refresh
          </button>
        </div>
        <DocumentsList />
      </div>
    </div>
  );
}

export default UploadBox;