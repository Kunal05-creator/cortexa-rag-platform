import { useState } from "react";
import UploadBox from "./components/UploadBox";
import ChatBox from "./components/ChatBox";

function App() {
  const [uploaded, setUploaded] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <header className="bg-black text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <h1 className="text-4xl font-bold">
            Cortexa
          </h1>

          <p className="text-gray-300 mt-2">
            Enterprise Knowledge Intelligence Platform
          </p>
        </div>
      </header>

      {/* Main Layout */}
      <main className="max-w-7xl mx-auto p-6">

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* Upload Panel */}
          <div className="lg:col-span-3">
            <UploadBox setUploaded={setUploaded} />
          </div>

          {/* Chat Panel */}
          <div className="lg:col-span-9">
            <ChatBox uploaded={uploaded} />
          </div>

        </div>

      </main>

    </div>
  );
}

export default App;