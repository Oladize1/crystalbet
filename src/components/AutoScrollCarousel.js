import React, { useEffect, useRef } from 'react';
import Banner from './Banner';
import dummyData from './DummyData';
import backgroundImage from '../assets/banner-bg.jpg';

const AutoScrollCarousel = () => {
  const carouselRef = useRef(null);

  useEffect(() => {
    const scrollCarousel = () => {
      if (carouselRef.current) {
        const { scrollLeft, clientWidth, scrollWidth } = carouselRef.current;
        const maxScrollLeft = scrollWidth - clientWidth;
        const nextScrollLeft = scrollLeft + clientWidth;

        if (nextScrollLeft >= maxScrollLeft) {
          carouselRef.current.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
          carouselRef.current.scrollBy({ left: clientWidth, behavior: 'smooth' });
        }
      }
    };

    const interval = setInterval(scrollCarousel, 6000);

    // Cleanup on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div ref={carouselRef} className="flex overflow-x-scroll scrollbar-hide w-full">
      {dummyData.map((data, index) => (
        <div
          key={index}
          className="flex-shrink-0 w-full bg-cover bg-center"
          style={{ backgroundImage: `url(${backgroundImage})` }}
        >
          <Banner {...data} />
        </div>
      ))}
    </div>
  );
};

export default AutoScrollCarousel;
