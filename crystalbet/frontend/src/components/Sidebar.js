import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="h-screen w-64 bg-white shadow-lg">
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-6">Menu</h2>
        <nav>
          <ul>
            <li className="mb-4">
              <Link to="/" className="text-lg text-gray-700 hover:text-red-600">
                Home
              </Link>
            </li>
            <li className="mb-4">
              <Link to="/live-bets" className="text-lg text-gray-700 hover:text-red-600">
                Live Bets
              </Link>
            </li>
            <li className="mb-4">
              <Link to="/bets" className="text-lg text-gray-700 hover:text-red-600">
                Bets
              </Link>
            </li>
            <li className="mb-4">
              <Link to="/profile" className="text-lg text-gray-700 hover:text-red-600">
                Profile
              </Link>
            </li>
            <li className="mb-4">
              <Link to="/login" className="text-lg text-gray-700 hover:text-red-600">
                Login
              </Link>
            </li>
            <li>
              <Link to="/signup" className="text-lg text-gray-700 hover:text-red-600">
                Sign Up
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
