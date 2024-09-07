import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { GiSoccerBall } from "react-icons/gi";
import { RiLiveFill } from "react-icons/ri";
import { FaRegCalendarCheck, FaRegCheckCircle, FaUserTie, FaRegFileAlt } from "react-icons/fa";
import { SlSupport } from "react-icons/sl";
import { CiSearch } from "react-icons/ci";
import { IoGiftSharp, IoNewspaperOutline, IoTimer } from "react-icons/io5";
import { LuLineChart } from "react-icons/lu";


const items = [
  { icon: <Link to={'sports/calcio'}><GiSoccerBall/></Link>, label: 'Calcio' },
  { icon: <Link to={'live'}><RiLiveFill/></Link>, label: 'Live' },
  { icon: '🎰', label: 'Casinò' },
  { icon: '🃏', label: 'Live Casinò' },
  { icon: '🎮', label: 'Virtuali' },
  { icon: <FaRegCalendarCheck/>, label: "Today's Matches" },
  { icon: <FaRegCheckCircle/>, label: "Coupon Check" },
  { icon: <SlSupport/>, label: "Help" },
  { icon: <FaUserTie/>, label: "Become an Agent" },
  { icon: <FaRegFileAlt/>, label: "How To Tutorials" },
  { icon: <CiSearch/>, label: "Search" },
  { icon: <IoGiftSharp/>, label: "Promotions" },
  { icon: <IoNewspaperOutline/>, label: "Blog" },
  { icon: <IoTimer/>, label: "Last Minute" },
  { icon: <LuLineChart/>, label: "Statistics" },
];

const Carousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const next = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 5) % items.length);
  };

  const prev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 5 + items.length) % items.length);
  };

  // useEffect(() => {
  //   const interval = setInterval(next, 3000); // Auto-scroll every 3 seconds
  //   return () => clearInterval(interval);
  // }, []);

  const currentItems = items.slice(currentIndex, currentIndex + 5);

  return (
    <div className="flex items-center w-full justify-between bg-accent text-secondary p-4 mt-16">
      <button onClick={prev} className="absolute left-0 z-10">
        ◀
      </button>
      <div className="flex justify-around w-full">
        {currentItems.map((item, index) => (
          <div key={index} className="flex flex-col items-center mx-2 cursor-pointer">
            <div className="text-3xl">{item.icon}</div>
            <div className='text-sm'>{item.label}</div>
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
