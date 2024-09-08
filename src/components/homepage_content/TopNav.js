import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { GiSoccerBall } from "react-icons/gi";
import { RiLiveFill } from "react-icons/ri";
import { FaRegCalendarCheck, FaLessThan ,FaRegCheckCircle, FaUserTie, FaRegFileAlt } from "react-icons/fa";
import { SlSupport } from "react-icons/sl";
import { CiSearch } from "react-icons/ci";
import { IoGiftSharp,  IoTimer } from "react-icons/io5";
import { LuLineChart } from "react-icons/lu";
import SearchModal from './../casino/Search'; 

const items = [
  { icon: <Link to={'sports/calcio'}><GiSoccerBall/></Link>, label: 'Calcio' },
  { icon: <Link to={'live'}><RiLiveFill/></Link>, label: 'Live' },
  { icon: <Link to={'casino'}>🎰</Link>, label: 'Casinò' },
  { icon: <Link to={'casino-live'}>🃏</Link>, label: 'Live Casinò' },
  { icon: <Link to={'virtuals'}>🎮</Link>, label: 'Virtuali' },
  { icon: <Link to={'todays-event'}><FaRegCalendarCheck/></Link>, label: "Today's Matches" },
  { icon: <Link to={'book-bet'}><FaRegCalendarCheck /></Link>, label: "Book A Bet"},
  { icon: <Link to={'coupon-check'}><FaRegCheckCircle/></Link>, label: "Coupon Check" },
  { icon: <Link to={'cms'}><SlSupport/></Link>, label: "Help" },
  { icon: <FaUserTie/>, label: "Become an Agent" },
  { icon: <FaRegFileAlt/>, label: "How To Tutorials" },
  { icon: <Link to={'odds-less-than'}><FaLessThan/></Link>, label: "Odds Less than" },
  { icon: <CiSearch/>, label: "Search" },  
  { icon: <IoGiftSharp/>, label: "Promotions" },
  { icon: <IoTimer/>, label: "Last Minute" },
  { icon: <LuLineChart/>, label: "Statistics" },
];

const Carousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showSearchModal, setShowSearchModal] = useState(false);

  const next = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 5) % items.length);
  };

  const prev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 5 + items.length) % items.length);
  };

  const handleSearchClick = () => {
    setShowSearchModal(true);  // Show the search modal when the search icon is clicked
  };

  const currentItems = items.slice(currentIndex, currentIndex + 5);

  return (
    <>
      <div className="flex items-center w-full justify-between bg-accent text-secondary p-4 mt-16">
        <button onClick={prev} className="absolute left-0 z-10">
          ◀
        </button>
        <div className="flex justify-around w-full">
          {currentItems.map((item, index) => (
            <div
              key={index}
              className="flex flex-col items-center mx-2 cursor-pointer"
              onClick={item.label === 'Search' ? handleSearchClick : undefined}  // Trigger search modal on click
            >
              <div className="text-3xl">{item.icon}</div>
              <div className='text-sm'>{item.label}</div>
            </div>
          ))}
        </div>
        <button onClick={next} className="absolute right-0 z-10">
          ▶
        </button>
      </div>

      {/* Conditionally render the search modal */}
      {showSearchModal && <SearchModal onClose={() => setShowSearchModal(false)} />}
    </>
  );
};

export default Carousel;
