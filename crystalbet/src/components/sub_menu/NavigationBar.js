// NavigationBar.js
import React  from 'react';
import { FaArrowLeft, FaFootballBall, FaLink, FaGift, FaDice } from 'react-icons/fa';

const NavigationBar = ({ activeItem, setActiveItem }) => {
  return (
    <div className="flex flex-col bg-accent text-white">
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
          className="w-full p-2 mb-4 rounded text-accent"
        />
      </div>
    </div>
  );
};

export default NavigationBar;
