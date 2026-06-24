import Sidebar from "./Sidebar";
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
    <div className="h-screen bg-[#212121] flex overflow-hidden">
      <Sidebar />

      <main className="flex flex-col flex-1 overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <ChatWindow
            messages={messages}
            loading={loading}
            timeline={timeline}
            blueprint={blueprint}
          />
        </div>

        <div className="border-t border-[#2F2F2F] bg-[#212121] px-6 py-5">
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