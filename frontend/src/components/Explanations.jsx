import React, { useEffect, useState } from "react";
import { getExplanations } from "../api/api.js";
import { FaUsers, FaUser } from "react-icons/fa";

const Explanations = ({ userId }) => {
  const [explanations, setExplanations] = useState([]);

  useEffect(() => {
    fetchExplanations();
  }, []);

  const fetchExplanations = async () => {
    const data = await getExplanations(userId);
    setExplanations(data.explanations || []);
  };

  const renderScoreCircle = (score) => {
    const radius = 18;
    const stroke = 3;
    const normalizedScore = Math.min(Math.max(score, 0), 10); // max 10
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (normalizedScore / 10) * circumference;

    return (
      <svg width={50} height={50}>
        <circle
          cx={25}
          cy={25}
          r={radius}
          stroke="#e5e7eb"
          strokeWidth={stroke}
          fill="none"
        />
        <circle
          cx={25}
          cy={25}
          r={radius}
          stroke="url(#grad)"
          strokeWidth={stroke}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 25 25)"
        />
        <defs>
          <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
        </defs>
        <text
          x="50%"
          y="50%"
          dominantBaseline="middle"
          textAnchor="middle"
          fontSize="12"
          fontWeight="bold"
          fill="#4f46e5"
        >
          {score.toFixed(1)}
        </text>
      </svg>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-extrabold mb-10 text-center text-gray-800">
        Recommendation Explanations
      </h1>
      <ul className="space-y-8">
        {explanations.map((item) => (
          <li
            key={item.item_id}
            className="backdrop-blur-sm bg-white/30 border border-gray-200 rounded-2xl shadow-lg p-6 hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-900">{item.title}</h2>
              <div>{renderScoreCircle(item.score)}</div>
            </div>

            <p className="text-gray-700 mb-4">{item.description}</p>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {item.tags.split(",").map((tag) => (
                <span
                  key={tag}
                  className="bg-gradient-to-r from-purple-100 to-indigo-100 text-purple-800 text-xs font-medium px-3 py-1 rounded-full shadow-sm"
                >
                  {tag}
                </span>
              ))}
            </div>

            {/* Community & Creator */}
            <div className="flex justify-between items-center text-gray-600 mb-4 text-sm">
              <span className="flex items-center gap-1">
                <FaUsers /> {item.community}
              </span>
              <span className="flex items-center gap-1">
                <FaUser /> {item.creator_name}
              </span>
            </div>

            {/* Reasons */}
            <div className="flex flex-wrap gap-2">
              {item.reasons.map((r, idx) => (
                <span
                  key={idx}
                  className="inline-block bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-medium shadow-sm"
                >
                  {r}
                </span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Explanations;
