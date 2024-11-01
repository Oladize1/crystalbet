import React, { useState } from 'react';
import GameSlots from './GameSlots';
import { FaArrowLeft } from 'react-icons/fa';

const CasinoPage = ({onFilterChange}) => {
  const [filter] = useState({ category: 'All', provider: '' }); 
  const [selectedCategory, setSelectedCategory] = useState('All');
 

  const categories = ['All', 'Evolution', 'N2Live', 'Portmaso', 'Spribe', 'VivoLive'];


  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
    onFilterChange(category); // Trigger filter change
  };

  return (
    <div className="flex flex-col bg-accent text-white my-12 h-full">
        <div className="flex justify-between items-center p-4 bg-accent">
        <button
          onClick={() => window.history.back()}
          className="flex items-center text-white"
        >
          <FaArrowLeft className="mr-2" /> Menù
        </button>
      </div>
        <div className="p-4">
        <input
          type="text"
          placeholder="Inserisci la tua ricerca"
          className="w-full p-2 mb-4 rounded text-accent"
        />
      </div>
      <div className="flex space-x-2 overflow-x-auto pb-2">
        {categories.map((category) => (
          <span
            key={category}
            onClick={() => handleCategoryClick(category)}
            className={`cursor-pointer px-2 py-1 rounded ${
              selectedCategory === category ? 'bg-accent text-white' : 'hover:text-primary-dark'
            }`}
          >
            {category}
          </span>
        ))}
      </div>
      <GameSlots filter={filter} />
    </div>
  );
};

export default CasinoPage;
