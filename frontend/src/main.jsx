import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles/globals.css";
import App from "./App";
import { BlueprintProvider } from "./context/BlueprintContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BlueprintProvider>
      <App />
    </BlueprintProvider>
  </StrictMode>
);