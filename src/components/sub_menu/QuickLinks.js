import React from 'react';

const links = [
  { name: 'Betslip', icon: '📄' },
  { name: 'Become an Agent', icon: '👤' },
  { name: 'Retail Site', icon: '🛒' },
  { name: 'Coupon Check', icon: '✅' },
  { name: 'Book a Bet', icon: '📑' },
  { name: 'Statistics', icon: '📊' },
  { name: 'Results', icon: '📊' },
  { name: 'News', icon: '📰' },
  { name: 'Less Than 2', icon: '⬅️' },
  { name: 'Contact Us', icon: '⬅️' },
  { name: 'Help', icon: '⬅️' },
];

const QuickLinks = () => {
  return (
    <div className="w-full bg-black text-white">
      {links.map((link, index) => (
        <div
          key={index}
          className="flex items-center justify-between px-4 py-3 border-t border-gray-700 cursor-pointer hover:bg-gray-800
        ">
          <span className="flex items-center gap-2">
            <span>{link.icon}</span> {link.name}
          </span>
          <span className="text-gray-500">{'>'}</span>
        </div>
      ))}
    </div>
  );
};

export default QuickLinks;
