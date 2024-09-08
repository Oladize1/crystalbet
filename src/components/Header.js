import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/logo1.png';

const Header = () => {
  return (
    <header className="bg-primary text-white px-1 fixed top-0 left-0 w-full h-16 flex items-center shadow-md z-50">
      <div className="container mx-auto flex justify-between items-center h-full">
        <Link to="/" className="text-xl font-bold flex items-center">
          <img src={Logo} alt="logo" className="w-16 h-auto md:w-24" /> 
        </Link>
        <nav className="flex items-center">
          <Link to="/login" className="ml-2 md:ml-4 font-bold text-secondary text-sm md:text-base">Login</Link>
          <Link to="/register" className="ml-2 md:ml-4 bg-secondary text-accent px-2 py-1 md:px-4 md:py-2 rounded-full font-bold text-sm md:text-base">Join</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
