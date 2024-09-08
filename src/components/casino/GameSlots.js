import React from 'react';
import './../../GameSlots.css';

const games = [
  { title: 'Game 1', description: 'Exciting slot game with great rewards', category: 'Videoslot', provider: 'Betsoft' },
  { title: 'Game 2', description: 'A thrilling adventure awaits', category: 'Table', provider: 'Netent' },
  // More game objects with category and provider fields...
];

const GameSlots = ({ filter }) => {
  // Filter games based on selected category and provider
  const filteredGames = games.filter(game => 
    (filter.category === 'All' || game.category === filter.category) &&
    (!filter.provider || game.provider === filter.provider)
  );

  return (
    <div className="games-container p-6 bg-gray-900">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {filteredGames.map((game, index) => (
          <div key={index} className="card-container">
            <div className="card">
              {/* this should be an image */}
              <div className="card-front bg-dark p-4 rounded overflow-hidden text-xs text-white">
                <h3 className="truncate">{game.title}</h3>
                <p className="truncate">{game.description}</p>
              </div>
              <div className="card-back bg-accent p-4 rounded flex items-center justify-center">
                <button className="login-button text-white border-2 border-white px-4 py-2 rounded hover:bg-white hover:text-accent transition duration-300">
                  LOGIN NOW
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GameSlots;
