import React, { useState } from 'react';
import NavigationBar from '../sub_menu/NavigationBar';
import CategoryFilter from './CategoryFilter'; // New component for categories and providers
import GameSlots from './GameSlots'; // New component for displaying the game slots

const CasinoPage = () => {
  const [activeItem, setActiveItem] = useState('Casinò'); // Set the default active item for Casino
  const [filter, setFilter] = useState({ category: 'All', provider: '' }); // State to manage the selected filters

  const handleFilterChange = (category, provider) => {
    setFilter({ category, provider });
    // Logic to filter the games based on selected category and provider
    // This logic can be handled within the GameSlots component using props or context
  };

  return (
    <div className="flex flex-col bg-accent text-white my-12 h-full">
      <NavigationBar activeItem={activeItem} setActiveItem={setActiveItem} />
      <CategoryFilter onFilterChange={handleFilterChange} />
      <GameSlots filter={filter} />
    </div>
  );
};

export default CasinoPage;
