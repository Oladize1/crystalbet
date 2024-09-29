import React from 'react';

const LiveBetList = ({ liveBets }) => {
  if (liveBets.length === 0) {
    return <div>No live bets available</div>;
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {liveBets.map((bet) => (
        <div key={bet.id} className="p-4 bg-white shadow rounded">
          <h3 className="text-xl font-bold">{bet.match}</h3>
          <p>Odds: {bet.odds}</p>
          <p>Stake: {bet.stake}</p>
        </div>
      ))}
    </div>
  );
};

export default LiveBetList;
