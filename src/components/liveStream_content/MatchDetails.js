// src/pages/MatchDetail.js
import React from 'react';
import { useLocation } from 'react-router-dom';

const MatchDetail = () => {
  const location = useLocation();
  const { match } = location.state || {}; // Get match data passed from BettingComponent

  if (!match) {
    return <div>No match selected.</div>;
  }

  return (
    <div className="bg-black text-white my-20 p-4">
      <h2 className="text-2xl font-bold mb-4">{`${match.team1} vs ${match.team2}`}</h2>
      
      <div className="mb-4">
        <h3 className="text-lg mb-2">1x2</h3>
        <div className="flex justify-between">
          {match.odds.map((odd, index) => (
            <button key={index} className="px-4 py-2 bg-gray-800 rounded-md w-full mx-2">
              {odd}
            </button>
          ))}
        </div>
      </div>
      
      {/* Add more betting options as needed */}
    </div>
  );
};

export default MatchDetail;
