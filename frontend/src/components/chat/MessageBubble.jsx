function MessageBubble({ sender, message }) {
  const isUser = sender === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div
          className="
            max-w-3xl
            bg-[#303030]
            text-white
            px-5
            py-3
            rounded-3xl
            text-[15px]
            leading-7
            whitespace-pre-wrap
          "
        >
          {message}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl text-white text-[15px] leading-7">
      {message}
    </div>
  );
}

export default MessageBubble;