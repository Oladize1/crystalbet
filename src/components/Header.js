import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/logo1.png';

const Header = () => {
  return (
    <header className="bg-primary text-white px-4 fixed top-0 left-0 w-full h-16 flex items-center shadow-md z-50">
      <div className="container mx-auto flex justify-between items-center h-full">
        <Link to="/" className="text-xl font-bold">
          <img src={Logo} alt="logo" className="w-24 h-auto" /> {/* Adjust width as needed */}
        </Link>
        <nav>
          <Link to="/login" className="ml-4 font-bold text-secondary">Login</Link>
          <Link to="/register" className="ml-4 bg-secondary text-accent px-4 py-2 rounded-full font-bold">Join</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
