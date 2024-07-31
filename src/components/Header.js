import React from 'react';


const Header = () => (
  <header className="bg-black text-white p-4 flex justify-between items-center sticky w-full">
    <div className="text-xl font-bold">
      <img className='w-24' src='./../images/logo.jpg' alt='kogo' />
    </div>
    <div className="flex space-x-4">
      <button className="font-semibold">Login</button>
      <button className="bg-red-600 font-semibold px-4 py-2 rounded-full">Join</button>
    </div>
  </header>
);

export default Header;
