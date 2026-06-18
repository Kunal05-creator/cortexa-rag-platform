import { useState } from "react";
import API from "../services/api";

function UploadBox({ setUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadPDF = async () => {
    if (!file) {
      setStatus("Please select a PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setStatus("Uploading and indexing document...");

      const res = await API.post("/upload", formData);

      setStatus(res.data.message);
      setUploaded(true);

    } catch (error) {
      console.error(error);
      setStatus("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-4 text-black">
        📄 Upload Document
      </h2>

      <p className="text-gray-500 mb-4">
        Upload a PDF to build your knowledge base.
      </p>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="w-full border rounded-lg p-2 mb-4"
      />

      {file && (
        <div className="mb-4 p-3 bg-gray-100 rounded-lg">
          <p className="font-medium">
            {file.name}
          </p>
          <p className="text-sm text-gray-500">
            {(file.size / 1024 / 1024).toFixed(2)} MB
          </p>
        </div>
      )}

      <button
        onClick={uploadPDF}
        disabled={loading}
        className="w-full bg-black text-white py-3 rounded-lg hover:bg-gray-800 transition"
      >
        {loading ? "Indexing..." : "Upload PDF"}
      </button>

      {status && (
        <div className="mt-4 p-3 rounded-lg bg-gray-100">
          {status}
        </div>
      )}

    </div>
  );
}

export default UploadBox;