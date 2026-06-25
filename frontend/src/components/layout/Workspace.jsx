import Sidebar from "./Sidebar";
import Header from "./Header";

import ChatWindow from "../chat/ChatWindow";
import PromptBox from "../chat/PromptBox";

function Workspace({
  onGenerate,
  loading,
  blueprint,
  messages,
  timeline,
}) {
  return (
    <div className="h-screen flex bg-[#171717] overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Workspace */}
      <main className="flex flex-col flex-1 bg-[#171717] overflow-hidden">
        {/* Top Header */}
        <Header />

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto">
          <ChatWindow
            messages={messages}
            timeline={timeline}
            blueprint={blueprint}
          />
        </div>

        {/* Prompt Box */}
        <div className="border-t border-[#262626] bg-[#171717] px-6 py-5 shrink-0">
          <div className="max-w-4xl mx-auto">
            <PromptBox
              onGenerate={onGenerate}
              loading={loading}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default Workspace;