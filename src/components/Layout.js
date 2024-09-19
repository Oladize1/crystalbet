import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Navbar from './Navbar';
import BackToTop from './BackToTop';

const Layout = ({ children }) => (
  <div className="w-min-screen flex flex-col">
    <Header />
    <main className="flex-grow">{children}</main>
    <Footer />
    <BackToTop />
    <Navbar />
  </div>
);

export default Layout;
