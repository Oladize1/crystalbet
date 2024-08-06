// src/components/SportsPage.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
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
  const navigate = useNavigate();

  return (
    <div className="flex flex-col bg-accent text-white my-12">
      <div className="flex flex-col">
        <div className="flex justify-between items-center p-4 bg-accent">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center text-white"
          >
            <FaArrowLeft className="mr-2" /> Menù
          </button>
        </div>
        <div className="flex justify-around items-center p-4 bg-accent">
          <div className="flex flex-col items-center cursor-pointer">
            <div className="bg-primary p-2 rounded-full mb-1">
              <FaFootballBall className="text-xl" />
            </div>
            <span>A-Z Sports</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-accent p-2 rounded-full mb-1">
              <FaLink className="text-xl" />
            </div>
            <span>Link veloci</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-accent p-2 rounded-full mb-1">
              <FaGift className="text-xl" />
            </div>
            <span>Promo</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-accent p-2 rounded-full mb-1">
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
        </div>
      </div>
    </div>
  );
};

export default SportsPage;
