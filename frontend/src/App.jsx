import { useState } from "react";
import UploadBox from "./components/UploadBox";
import ChatBox from "./components/ChatBox";

function App() {
  const [uploaded, setUploaded] = useState(false);

  return (
    <div className="min-h-screen bg-black text-white">

      {/* Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 left-0 w-[700px] h-[700px] bg-purple-700/20 blur-[200px]" />
        <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-fuchsia-700/20 blur-[200px]" />
      </div>

      {/* Header */}
      <header className="h-20 border-b border-purple-900/30 flex items-center justify-between px-8 backdrop-blur-xl">
        <div>
          <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-fuchsia-500 bg-clip-text text-transparent">
            CORTEXA
          </h1>
          <p className="text-sm text-slate-400">
            Enterprise Knowledge Intelligence
          </p>
        </div>
        {/* Removed the "+ New Chat" button */}
      </header>

      {/* Layout */}
      <div className="h-[calc(100vh-80px)] flex">

        {/* LEFT SIDEBAR – REMOVED (chat history) */}

        {/* Upload Section */}
        <section className="w-80 border-r border-purple-900/30 overflow-y-auto">
          <UploadBox setUploaded={setUploaded} />
        </section>

        {/* Chat Section */}
        <main className="flex-1 overflow-hidden">
          <ChatBox uploaded={uploaded} />
        </main>

      </div>
    </div>
  );
}

export default App;