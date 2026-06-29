import axios from "axios";

const API_BASE = "http://localhost:8000";

export const generateBlueprint = async (idea) => {
  try {
    const response = await axios.post(
      `${API_BASE}/generate`,
      {
        idea: idea,
      }
    );

    return response.data;
  } catch (error) {
    console.error("API Error:", error.response?.data || error.message);
    throw error;
  }
};

export const generateBlueprintStream = (
  idea,
  onAgentEvent,
  onResult,
  onError
) => {
  const url = `${API_BASE}/generate-stream?idea=${encodeURIComponent(idea)}`;
  const source = new EventSource(url);

  source.addEventListener("agent", (event) => {
    try {
      const payload = JSON.parse(event.data);
      onAgentEvent?.(payload);
    } catch (parseError) {
      console.error("Failed to parse SSE agent payload:", parseError);
    }
  });

  source.addEventListener("result", (event) => {
    try {
      const payload = JSON.parse(event.data);
      onResult?.(payload);
    } catch (parseError) {
      console.error("Failed to parse SSE result payload:", parseError);
    } finally {
      source.close();
    }
  });

  source.addEventListener("error", (event) => {
    try {
      const payload = JSON.parse(event.data || "{}");
      onError?.(payload.message || "An unknown error occurred.");
    } catch (parseError) {
      console.error("Failed to parse SSE error payload:", parseError);
      onError?.("An unknown error occurred.");
    } finally {
      source.close();
    }
  });

  source.onerror = () => {
    onError?.("Connection error while receiving live agent updates.");
    source.close();
  };

  return source;
};