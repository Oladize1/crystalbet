// src/components/SportsPage.jsx
import React, { useState } from 'react';
import QuickLinks from './QuickLinks';
import { FaArrowLeft, FaFootballBall, FaLink, FaGift, FaDice } from 'react-icons/fa';

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
        return <QuickLinks/>;
      case 'Promo':
        return <div>Promo content goes here</div>;
      case 'Casinò':
        return <div>Casinò content goes here</div>;
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col bg-accent text-white my-12 h-full">
      <div className="flex flex-col">
        <div className="flex justify-between items-center p-4 bg-accent">
          <button
            onClick={() => window.history.back()}
            className="flex items-center text-white"
          >
            <FaArrowLeft className="mr-2" /> Menù
          </button>
        </div>
        <div className="flex justify-around items-center p-4 bg-accent">
          <div
            className="flex flex-col items-center cursor-pointer"
            onClick={() => setActiveItem('A-Z Sports')}
          >
            <div
              className={`${
                activeItem === 'A-Z Sports' ? 'bg-primary' : 'bg-accent'
              } p-2 rounded-full mb-1`}
            >
              <FaFootballBall className="text-xl" />
            </div>
            <span>A-Z Sports</span>
          </div>
          
          <div
            className="flex flex-col items-center cursor-pointer"
            onClick={() => setActiveItem('Link veloci')}
          >
            <div
              className={`${
                activeItem === 'Link veloci' ? 'bg-primary' : 'bg-accent'
              } p-2 rounded-full mb-1`}
            >
              <FaLink className="text-xl" />
            </div>
            <span>Link veloci</span>
          </div>
          
          <div
            className="flex flex-col items-center cursor-pointer"
            onClick={() => setActiveItem('Promo')}
          >
            <div
              className={`${
                activeItem === 'Promo' ? 'bg-primary' : 'bg-accent'
              } p-2 rounded-full mb-1`}
            >
              <FaGift className="text-xl" />
            </div>
            <span>Promo</span>
          </div>
          <div
            className="flex flex-col items-center cursor-pointer"
            onClick={() => setActiveItem('Casinò')}
          >
            <div
              className={`${
                activeItem === 'Casinò' ? 'bg-primary' : 'bg-accent'
              } p-2 rounded-full mb-1`}
            >
              <FaDice className="text-xl" />
            </div>
            <span>Casinò</span>
          </div>
        </div>
        <div className="p-4">
          <input
            type="text"
            placeholder="Inserisci la tua ricerca"
            className="w-full p-2 mb-4 rounded"
          />
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default SportsPage;
