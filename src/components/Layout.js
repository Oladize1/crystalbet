// src/components/Layout.jsx
import React from 'react';
import Header from './Header';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-accent">
      <Header />
      <div className="flex-grow">
        {children}
      </div>
      <Navbar />
    </div>
  );
};

export default Layout;
