import React, { useState, useEffect } from 'react';

const items = [
  { icon: '⚽', label: 'Calcio' },
  { icon: '📺', label: 'Live' },
  { icon: '🎰', label: 'Casinò' },
  { icon: '🃏', label: 'Live Casinò' },
  { icon: '🎮', label: 'Virtuali' },
  { icon: '🏀', label: 'Basketball' },
  { icon: '🎾', label: 'Tennis' },
  { icon: '🏈', label: 'Football' },
  { icon: '⚾', label: 'Baseball' },
  { icon: '🏒', label: 'Hockey' },
];

const Carousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const next = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 5) % items.length);
  };

  const prev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 5 + items.length) % items.length);
  };

  useEffect(() => {
    const interval = setInterval(next, 3000); // Auto-scroll every 3 seconds
    return () => clearInterval(interval);
  }, []);

  const currentItems = items.slice(currentIndex, currentIndex + 5);

  return (
    <div className="relative flex items-center justify-between bg-gray-800 text-white p-4">
      <button onClick={prev} className="absolute left-0 z-10">
        ◀
      </button>
      <div className="flex justify-around w-full">
        {currentItems.map((item, index) => (
          <div key={index} className="flex flex-col items-center mx-2">
            <div className="text-3xl">{item.icon}</div>
            <div>{item.label}</div>
          </div>
        ))}
      </div>
      <button onClick={next} className="absolute right-0 z-10">
        ▶
      </button>
    </div>
  );
};

export default Carousel;
