import React from 'react';

const Header = () => (
  <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
    <div className="text-xl font-bold">CRYSTALBET</div>
    <div className="flex space-x-4">
      <button className="font-semibold">Login</button>
      <button className="bg-red-600 font-semibold px-4 py-2 rounded-full">Join</button>
    </div>
  </header>
);

export default Header;
