import React from 'react';

const Header = () => (
  <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
    <div className="text-xl font-bold">NEOBET</div>
    <nav>
      <ul className="flex space-x-4">
        <li><a href="#home" className="hover:underline">Home</a></li>
        <li><a href="#how-to" className="hover:underline">How to Bet</a></li>
        <li><a href="#odds" className="hover:underline">Odds</a></li>
        <li><a href="#search" className="hover:underline">Search</a></li>
      </ul>
    </nav>
    <div className="flex space-x-4">
      <button className="bg-green-500 px-4 py-2 rounded">Login</button>
      <button className="bg-yellow-500 px-4 py-2 rounded">Join</button>
    </div>
  </header>
);

export default Header;
