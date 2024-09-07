import React from 'react';
import { Link } from 'react-router-dom';
import { FaBars, FaVideo, FaClipboardList, FaRegCalendarCheck, FaUserPlus } from 'react-icons/fa';

const BottomNav = () => {
  return (
    <div className="fixed cursor-pointer bottom-0 w-full bg-black text-white text-sm flex justify-around items-center py-2">
      <Link to='/AZMenu' className="flex flex-col items-center">
        <FaBars size={24} />
        <span>Menù</span>
      </Link>
      <Link to='/live'>
      <div className="flex flex-col items-center">
        <FaVideo size={24} />
        <span>Live</span>
      </div>
      </Link>
      <Link to="/betslip">
      <div className="flex flex-col items-center">
        <FaClipboardList size={24} />
        <span>Schedina</span>
      </div>
      </Link>
      <Link to="/book-bet">
      <div className="flex flex-col items-center">
        <FaRegCalendarCheck size={24} />
        <span>Scommesse prenotate</span>
      </div>
      </Link>
      <Link to='/register' className="flex flex-col items-center">
        <FaUserPlus size={24} />
        <span>Registrati</span>
      </Link>
    </div>
  );
};

export default BottomNav;
