import React from 'react';

const BetHistory = ({ betHistory }) => {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="text-xl font-bold mb-4">Your Bet History</h3>
      <ul>
        {betHistory.map((bet) => (
          <li key={bet.id} className="mb-2">
            <div className="flex justify-between">
              <span>{bet.title}</span>
              <span>{bet.status}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BetHistory;
