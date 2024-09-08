// SportsPage.js
import React, { useState } from 'react';
import QuickLinks from './QuickLinks';
import Promo from './Promo';
import NavigationBar from './NavigationBar'; // Import the new NavigationBar component

const sports = [
  { name: 'Calcio', count: 562 },
  { name: 'Baseball', count: 26 },
  { name: 'Hockey', count: 6 },
  { name: 'Tennis', count: 134 },
  { name: 'Pallamano', count: 4 },
  { name: 'Pugilato', count: 11 },
  { name: 'Rugby', count: 1 },
];

const SportsPage = () => {
  const [activeItem, setActiveItem] = useState('A-Z Sports');

  const renderContent = () => {
    switch (activeItem) {
      case 'A-Z Sports':
        return (
          <ul>
            {sports.map((sport) => (
              <li
                key={sport.name}
                className="flex justify-between items-center p-4 border-b border-accent"
              >
                <span>{sport.name}</span>
                <span>{sport.count}</span>
              </li>
            ))}
          </ul>
        );
      case 'Link veloci':
        return <QuickLinks />;
      case 'Promo':
        return <Promo />;
      case 'Casinò':
        return <div>Casinò content goes here</div>;
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col bg-accent text-white my-12 h-full">
      <NavigationBar activeItem={activeItem} setActiveItem={setActiveItem} />
      <div className="p-4">
        {renderContent()}
      </div>
    </div>
  );
};

export default SportsPage;
