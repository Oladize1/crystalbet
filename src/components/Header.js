import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/logo1.png';

const Header = () => {
  return (
    <header className="bg-primary text-white px-4 fixed top-0 left-0 w-full h-16 flex items-center shadow-md z-50">
      <div className="container mx-auto flex justify-between items-center h-full">
        <Link to="/" className="text-xl font-bold flex items-center">
          <img src={Logo} alt="logo" className="w-12 h-auto md:w-16 lg:w-24" />
        </Link>
        <nav className="flex items-center">
          <Link to="/login" className="ml-3 md:ml-6 font-bold text-secondary text-sm md:text-base lg:text-lg">Login</Link>
          <Link to="/register" className="ml-3 md:ml-6 bg-secondary text-accent px-3 py-1 md:px-4 md:py-2 lg:px-6 lg:py-3 rounded-full font-bold text-sm md:text-base lg:text-lg">Join</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
