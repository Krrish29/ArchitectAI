function Header() {
  return (
    <header className="h-20 border-b border-[#30363D]">
      <div className="h-full max-w-5xl mx-auto px-10 flex items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">
            ArchitectAI
          </h1>

          <p className="text-gray-400">
            Your AI Engineering Manager
          </p>
        </div>
      </div>
    </header>
  );
}

export default Header;