import React, { useEffect, useState } from "react";
import { getHomefeed, sendFeedback } from "../api/api.js";
import { FaThumbsUp, FaEye, FaShareAlt } from "react-icons/fa";

const HomeFeed = ({ userId }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [feedbackMsg, setFeedbackMsg] = useState("");

  useEffect(() => {
    fetchHomefeed();
  }, []);

  const fetchHomefeed = async () => {
    const data = await getHomefeed(userId);
    setRecommendations(data.recommendations || []);
    console.log(data)
  };

  const handleFeedback = async (itemId, feedbackType) => {
    try {
      const response = await sendFeedback({ user_id: userId, item_id: itemId, feedback_type: feedbackType });

      setRecommendations(prev =>
        prev.map(item =>
          item.item_id === itemId
            ? { ...item, score: item.score + (feedbackType === "like" ? 1 : feedbackType === "view" ? 0.5 : 0.2) }
            : item
        )
      );

      setFeedbackMsg(`Your "${feedbackType}" feedback for item ${itemId} was recorded!`);
      setTimeout(() => setFeedbackMsg(""), 3000);

    } catch (err) {
      console.error(err);
      setFeedbackMsg("Failed to send feedback. Try again!");
      setTimeout(() => setFeedbackMsg(""), 3000);
    }
  };


  return (
    <div className="max-w-5xl mx-auto p-6">
      {feedbackMsg && (
        <div className="bg-green-100 text-green-800 p-3 rounded mb-4 text-center font-medium shadow">
          {feedbackMsg}
        </div>
      )}
      <h1 className="text-4xl font-extrabold mb-10 text-center text-gray-800">
        Recommendation HomeFeed
      </h1>
      <div className="grid md:grid-cols-2 gap-6">
        {recommendations.map((item) => (
          <div
            key={item.item_id}
            className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 p-6 flex flex-col justify-between"
          >
            <div>
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-xl font-semibold text-gray-800">Item {item.item_id}</h2>
                <span className="bg-indigo-100 text-indigo-700 font-semibold px-3 py-1 rounded-full text-sm">
                  Score: {item.score.toFixed(2)}
                </span>
              </div>
              <p className="text-gray-600 mb-4">
                {item.reasons && item.reasons.length > 0
                  ? item.reasons.join(", ")
                  : "Recommended for you"}
              </p>
            </div>
            <div className="flex space-x-3 mt-4">
              <button
                onClick={() => handleFeedback(item.item_id, "like")}
                className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 hover:bg-blue-600 transition"
              >
                <FaThumbsUp /> Like
              </button>
              <button
                onClick={() => handleFeedback(item.item_id, "view")}
                className="flex-1 bg-green-500 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 hover:bg-green-600 transition"
              >
                <FaEye /> View
              </button>
              <button
                onClick={() => handleFeedback(item.item_id, "share")}
                className="flex-1 bg-purple-500 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 hover:bg-purple-600 transition"
              >
                <FaShareAlt /> Share
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomeFeed;
