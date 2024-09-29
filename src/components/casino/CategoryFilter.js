import React, { useState } from 'react';

const CategoryFilter = ({ onFilterChange }) => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedProvider, setSelectedProvider] = useState(''); // No provider selected by default

  const categories = ['All', 'Generic', 'Popular', 'New', 'Hot', 'Table', 'Poker', 'Roulette', 'Keno & Bingo', 'Videoslot'];
  const providers = [
    '1x2', 'Amatic', 'Betsoft', 'Bomba', 'Booming', 'Booongo', 'Casino Technology', 'EGT', 'Evoplay', 'GameArt', 'Gaminator', 
    'Habanero', 'IGrosoft', 'IGT', 'IronDog', 'ISoftBet', 'Merkur', 'Netent', 'Novomatic', 'Octavian', 'Platipus', 'PlayNGo', 
    'Playson', 'Pragmatic', 'Quickspin', 'RedRake', 'Skywind', 'Spinmatic', 'Spinomenal', 'UpGaming', 'Xplosive', 'Yggdrasil', 
    'Zeus Play'
  ];

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
    onFilterChange(category, selectedProvider); // Trigger filter change
  };

  const handleProviderClick = (provider) => {
    setSelectedProvider(provider);
    onFilterChange(selectedCategory, provider); // Trigger filter change
  };

  return (
    <div className="p-2 bg-dark text-white text-xs overflow-hidden">
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
      <div className="flex space-x-2 overflow-x-auto pb-2 mt-2">
        {providers.map((provider) => (
          <span
            key={provider}
            onClick={() => handleProviderClick(provider)}
            className={`cursor-pointer px-2 py-1 rounded ${
              selectedProvider === provider ? 'bg-accent text-white' : 'hover:text-primary-dark'
            }`}
          >
            {provider}
          </span>
        ))}
      </div>
    </div>
  );
};

export default CategoryFilter;
