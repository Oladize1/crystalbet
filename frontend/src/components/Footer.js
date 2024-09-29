// Footer.js
import React from 'react';
import { FaFacebook, FaInstagram, FaLinkedin } from 'react-icons/fa';
import { FaXTwitter } from "react-icons/fa6";

const Footer = () => (
  <footer className="text-white py-6 mb-10 bg-accent">
    <div className="container mx-auto px-4">
      <div className="flex justify-between items-center flex-col gap-6">
        <div className="flex items-center space-x-2">
          <span className="text-secondary ring-2 ring-primary p-2 rounded-full">18+</span>
          <span>Play responsibly</span>
        </div>
        <div className="flex justify-between items-center gap-96 max-lg:gap-4">
          <FaFacebook className="text-2xl cursor-pointer" />
          <FaXTwitter className="text-2xl cursor-pointer" />
          <FaInstagram className="text-2xl cursor-pointer" />
          <FaLinkedin className="text-2xl cursor-pointer" />
        </div>
      </div>
      <div className="text-center mt-6">
        <h2 className='font-bold'>CrystalBet</h2>
        <p>© 2020. All rights reserved.</p>
        <p className="text-primary">v1.4.74</p>
      </div>
    </div>
  </footer>
);

export default Footer;
