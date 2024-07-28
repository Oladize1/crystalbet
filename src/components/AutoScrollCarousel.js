// AutoScrollCarousel.js
import React, { useEffect, useRef } from 'react';
import Banner from './Banner';

const AutoScrollCarousel = () => {
  const carouselRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      if (carouselRef.current) {
        carouselRef.current.scrollBy({ left: 200, behavior: 'smooth' });
      }
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const banners = Array(5).fill(<Banner />); // Repeat the Banner component 5 times

  return (
    <div ref={carouselRef} className="flex overflow-x-scroll scrollbar-hide">
      {banners.map((banner, index) => (
        <div key={index} className="min-w-[200px]">
          {banner}
        </div>
      ))}
    </div>
  );
};

export default AutoScrollCarousel;
