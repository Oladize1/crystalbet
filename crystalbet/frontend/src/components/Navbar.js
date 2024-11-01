import React from 'react';
import { Link } from 'react-router-dom';
import { FaBars, FaVideo, FaClipboardList, FaRegCalendarCheck, FaUserPlus } from 'react-icons/fa';

const BottomNav = () => {
  return (
    <div className="fixed cursor-pointer bottom-0 w-full bg-black text-white text-xs flex justify-around items-center py-3 md:py-4 lg:py-3">
      <Link to='/AZMenu' className="flex flex-col items-center hover:text-primary-dark">
        <FaBars size={20} className="transition-transform duration-300 ease-in-out hover:scale-110" />
        <span className="text-[10px] md:text-[12px] lg:text-sm">Menu</span>
      </Link>
      <Link to='/live' className="flex flex-col items-center hover:text-primary-dark">
        <FaVideo size={20} className="transition-transform duration-300 ease-in-out hover:scale-110" />
        <span className="text-[10px] md:text-[12px] lg:text-sm">Live</span>
      </Link>
      <Link to="/betslip" className="flex flex-col items-center hover:text-primary-dark">
        <FaClipboardList size={20} className="transition-transform duration-300 ease-in-out hover:scale-110" />
        <span className="text-[10px] md:text-[12px] lg:text-sm">Betslip</span>
      </Link>
      <Link to="/book-bet" className="flex flex-col items-center hover:text-primary-dark">
        <FaRegCalendarCheck size={20} className="transition-transform duration-300 ease-in-out hover:scale-110" />
        <span className="text-[10px] md:text-[12px] lg:text-sm">Book A Bet</span>
      </Link>
      <Link to='/register' className="flex flex-col items-center hover:text-primary-dark">
        <FaUserPlus size={20} className="transition-transform duration-300 ease-in-out hover:scale-110" />
        <span className="text-[10px] md:text-[12px] lg:text-sm">Register</span>
      </Link>
    </div>
  );
};

export default BottomNav;
