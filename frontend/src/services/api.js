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