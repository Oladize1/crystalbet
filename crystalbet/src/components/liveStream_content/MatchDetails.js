import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const MatchDetail = () => {
  const location = useLocation();
  const { match } = location.state || {}; 
  const [searchTerm, setSearchTerm] = useState('');
  const [bettingMarkets, setBettingMarkets] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch betting markets for the match from the backend if needed
    const fetchMarkets = async () => {
      try {
        const response = await fetch(`/api/matches/${match.id}/markets`);
        if (!response.ok) {
          throw new Error('Markets not found');
        }
        const data = await response.json();
        setBettingMarkets(data);
      } catch (error) {
        setError(error.message);
      }
    };

    if (match && match.id) {
      fetchMarkets();
    }
  }, [match]);

  if (!match) {
    return <div>No match selected.</div>;
  }

  const filteredMarkets = bettingMarkets.filter(market =>
    market.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-accent-dark text-secondary-dark my-16 p-4 rounded-md shadow-md">
      <h2 className="text-3xl font-bold mb-4">{`${match.team_a} vs ${match.team_b}`}</h2>
      <h3 className="text-lg mb-6">{match.time}</h3>

      <input
        type="text"
        placeholder="Filtro probabilità per nome"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        className="w-full mb-6 p-2 bg-accent-light text-secondary-dark rounded-md"
      />

      {filteredMarkets.map((market, index) => (
        <div key={index} className="mb-6">
          <div className="flex justify-between items-center bg-accent-light p-3 rounded-md mb-2">
            <h3 className="text-lg font-bold">{market.label}</h3>
            <button className="text-sm bg-accent-dark text-secondary-light px-3 py-1 rounded-full">i</button>
          </div>
        </div>
      ))}
      {filteredMarkets.length === 0 && (
        <div className="text-secondary-dark p-4">No markets found for "{searchTerm}"</div>
      )}
    </div>
  );
};

export default MatchDetail;
