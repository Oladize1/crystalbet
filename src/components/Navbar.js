import React from 'react';
import { FaBars, FaVideo, FaClipboardList, FaRegCalendarCheck, FaUserPlus } from 'react-icons/fa';

const BottomNav = () => {
  return (
    <div className="fixed bottom-0 w-full bg-black text-white flex justify-around items-center py-2">
      <div className="flex flex-col items-center">
        <FaBars size={24} />
        <span>Menu</span>
      </div>
      <div className="flex flex-col items-center">
        <FaVideo size={24} />
        <span>Live</span>
      </div>
      <div className="flex flex-col items-center">
        <FaClipboardList size={24} />
        <span>Schedina</span>
      </div>
      <div className="flex flex-col items-center">
        <FaRegCalendarCheck size={24} />
        <span>Scommesse prenotate</span>
      </div>
      <div className="flex flex-col items-center">
        <FaUserPlus size={24} />
        <span>Registrati</span>
      </div>
    </div>
  );
};

export default BottomNav;
