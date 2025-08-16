import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const getHomefeed = async (userId) => {
  const res = await fetch(`${API_URL}/homefeed?user_id=${userId}`, {
    method: 'GET',
    headers: {"Content-Type": "application/json"}
  });
  console.log(res.json)
  return res.json();
};

export const sendFeedback = async ({ user_id, item_id, feedback_type }) => {
  const res = await fetch(`${API_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, item_id, feedback_type }),
  });
  return res.json();
};

export const getExplanations = async (user_id, top_k=10) => {
  const res = await axios.get(`${API_URL}/explanations`, { params: { user_id, top_k } });
  console.log(res.data)
  return res.data;
};
