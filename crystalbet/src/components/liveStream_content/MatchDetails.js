import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

const MatchDetail = () => {
  const location = useLocation();
  const { match } = location.state || {}; // Get match data passed from BettingComponent
  
  // State to handle search input
  const [searchTerm, setSearchTerm] = useState('');

  if (!match) {
    return <div>No match selected.</div>;
  }

  // List of betting markets to display
  const bettingMarkets = [
    { name: "1x2", label: "1x2" },
    { name: "Prossimo Goal 1", label: "Next Goal 1" },
    { name: "Ultimo Goal", label: "Last Goal" },
    { name: "Double Chance", label: "DC" }
  ];

  // Filter markets based on search term
  const filteredMarkets = bettingMarkets.filter(market =>
    market.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-accent-dark text-secondary-dark my-16 p-4 rounded-md shadow-md">
      <h2 className="text-3xl font-bold mb-4">{`${match.team1} vs ${match.team2}`}</h2>
      <h3 className="text-lg mb-6">{match.time}</h3>

      {/* Search bar */}
      <input
        type="text"
        placeholder="Filtro probabilità per nome" // Italian for "Filter probabilities by name"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        className="w-full mb-6 p-2 bg-accent-light text-secondary-dark rounded-md"
      />

      {/* Betting Markets Layout */}
      {filteredMarkets.map((market, index) => (
        <div key={index} className="mb-6">
          <div className="flex justify-between items-center bg-accent-light p-3 rounded-md mb-2">
            <h3 className="text-lg font-bold">{market.label}</h3>
            {/* Toggle button to expand/collapse market odds */}
            <button className="text-sm bg-accent-dark text-secondary-light px-3 py-1 rounded-full">i</button>
          </div>
          
          {/* Display odds for the market in a horizontal format */}
          {match.odds[market.name] ? (
            <div className="grid grid-cols-3 gap-4">
              {match.odds[market.name].map((odd, oddIndex) => (
                <div
                  key={oddIndex}
                  className="flex items-center justify-between bg-accent-light p-4 rounded-md"
                >
                  <div className="font-bold">{odd}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-secondary-dark p-4">No odds available for {market.label}</div>
          )}
        </div>
      ))}

      {/* Fallback if no markets match the search term */}
      {filteredMarkets.length === 0 && (
        <div className="text-secondary-dark p-4">No markets found for "{searchTerm}"</div>
      )}
    </div>
  );
};

export default MatchDetail;
