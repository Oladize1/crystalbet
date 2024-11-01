import React from 'react';

const BetList = ({ bets }) => {
  return (
    <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
      {bets.map((bet) => (
        <div key={bet.id} className="bg-white p-4 rounded shadow">
          <h3 className="text-xl font-bold mb-2">{bet.title}</h3>
          <p className="mb-4">{bet.description}</p>
          <button className="bg-red-500 text-white p-2 rounded">Place Bet</button>
        </div>
      ))}
    </div>
  );
};

export default BetList;
