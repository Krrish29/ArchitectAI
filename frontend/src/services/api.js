import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const generateBlueprint = async (idea) => {
  const response = await api.post("/generate", {
    idea,
  });

  return response.data;
};

export default api;