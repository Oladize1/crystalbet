import React, { useState } from 'react';

const HelpPage = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <div className="mt-20 pt-1 px-3">
      <div className="flex items-center text-primary cursor-pointer">
        <button onClick={() => window.history.back()} className="mr-2">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M15 19l-7-7 7-7"
            ></path>
          </svg>
        </button>
        <h1 className="text-xl">Help</h1>
      </div>

      <div className="mt-4 space-y-4">
        <div className="bg-accent-dark p-4 rounded-md text-gray-300">
          ABOUT US
        </div>

        <div className="bg-accent-dark p-4 rounded-md text-gray-300">
          TERMS & CONDITIONS
        </div>

        <div className="bg-primary-dark p-4 rounded-md text-secondary cursor-pointer" onClick={toggleDropdown}>
          <div className="flex justify-between items-center">
            <span>RULES ON SPORTS BET</span>
            <svg
              className={`w-5 h-5 transform transition-transform duration-300 ${
                isDropdownOpen ? 'rotate-180' : ''
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </div>
        </div>

        {isDropdownOpen && (
          <div className="space-y-2 pl-6">
            <div className="bg-accent-dark p-4 rounded-md text-gray-300">
              ACCEPTANCE OF BETS
            </div>
            <div className="bg-accent-dark p-4 rounded-md text-gray-300">
              SPORTS RULES
            </div>
          </div>
        )}

        <div className="bg-accent-dark p-4 rounded-md text-gray-300">
          CONTACT US!
        </div>
      </div>
    </div>
  );
};

export default HelpPage;
