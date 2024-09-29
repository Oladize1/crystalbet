import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { GiSoccerBall } from "react-icons/gi";
import { RiLiveFill } from "react-icons/ri";
import { FaRegCalendarCheck, FaLessThan, FaRegCheckCircle, FaUserTie, FaRegFileAlt } from "react-icons/fa";
import { SlSupport } from "react-icons/sl";
import { RiFileTextLine } from 'react-icons/ri';
import { CiSearch } from "react-icons/ci";
import { IoGiftSharp, IoTimer } from "react-icons/io5";
import { LuLineChart } from "react-icons/lu";
import SearchModal from './../casino/Search';
import { motion } from 'framer-motion';
import { useMediaQuery } from 'react-responsive';

const items = [
  { icon: <Link to={'sports/football'}><GiSoccerBall /></Link>, label: 'Football' },
  { icon: <Link to={'live'}><RiLiveFill /></Link>, label: 'Live' },
  { icon: <Link to={'casino'}>🎰</Link>, label: 'Casino' },
  { icon: <Link to={'casino-live'}>🃏</Link>, label: 'Live Casino' },
  { icon: <Link to={'virtuals'}>🎮</Link>, label: 'Virtuals' },
  { icon: <Link to={'todays-event'}><FaRegCalendarCheck /></Link>, label: "Today's Matches" },
  { icon: <Link to={'book-bet'}><div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
    <RiFileTextLine style={{ fontSize: '24px', position: 'relative' }} />
  </div></Link>, label: "Book A Bet" },
  { icon: <Link to={'coupon-check'}><FaRegCheckCircle /></Link>, label: "Coupon Check" },
  { icon: <Link to={'cms'}><SlSupport /></Link>, label: "Help" },
  { icon: <FaUserTie />, label: "Become an Agent" },
  { icon: <FaRegFileAlt />, label: "How To Tutorials" },
  { icon: <Link to={'odds-less-than'}><FaLessThan /></Link>, label: "Odds Less Than" },
  { icon: <CiSearch />, label: "Search" },
  { icon: <IoGiftSharp />, label: "Promotions" },
  { icon: <IoTimer />, label: "Last Minute" },
  { icon: <LuLineChart />, label: "Statistics" },
];

const Carousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showSearchModal, setShowSearchModal] = useState(false);

  const isSmallScreen = useMediaQuery({ query: '(max-width: 640px)' });
  const itemsToShow = isSmallScreen ? 3 : 5;

  const next = () => {
    setCurrentIndex((prevIndex) => (prevIndex + itemsToShow) % items.length);
  };

  const prev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - itemsToShow + items.length) % items.length);
  };

  const handleSearchClick = () => {
    setShowSearchModal(true);
  };

  const currentItems = items.slice(currentIndex, currentIndex + itemsToShow);

  return (
    <>
      <div className="flex items-center w-full justify-between bg-accent text-secondary p-6 mt-16 relative overflow-hidden">
        <button onClick={prev} className="absolute left-0 z-10">
          ◀
        </button>
        <div className="w-full overflow-hidden">
          <motion.div
            className="flex justify-around"
            initial={{ x: "-100%" }}
            animate={{ x: "0%" }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            key={currentIndex}
          >
            {currentItems.map((item, index) => (
              <motion.div
                key={index}
                className="flex flex-col items-center justify-center mx-2 cursor-pointer transform transition-transform duration-300 hover:scale-100"
                style={{ height: '80px', width: '60px' }} // Set uniform height and width
                whileHover={{ scale: 1.05 }}
                onClick={item.label === 'Search' ? handleSearchClick : undefined}
              >
                <div className="flex items-center justify-center text-2xl mb-2" style={{ height: '40px', width: '40px' }}>
                  {item.icon}
                </div>
                <div className="text-sm text-center">{item.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
        <button onClick={next} className="absolute right-0 z-10">
          ▶
        </button>
      </div>

      {showSearchModal && <SearchModal onClose={() => setShowSearchModal(false)} />}
    </>
  );
};

export default Carousel;
