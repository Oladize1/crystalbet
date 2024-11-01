import React, { useState } from 'react';

const QuickBet = () => {
  const [code, setCode] = useState('');
  const [selection, setSelection] = useState('');

  const options = ['Option 1', 'Option 2', 'Option 3'];

  return (
    <div className="flex flex-col items-center justify-center mt-16">
      {/* Quick Bet section */}
      <div className="w-full bg-dark-secondary p-2 mt-6 rounded-md">
        <h2 className="text-white mb-4 text-left">Quick Bet</h2>

        {/* Input and Dropdown */}
        <div className="flex space-x-2 mb-4">
          {/* Code Input (1/3 width) */}
          <input
            type="text"
            placeholder="Code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-1/3 p-3 text-black text-lg rounded-md placeholder-gray-500"
          />

          {/* Dropdown (2/3 width) */}
          <select
            value={selection}
            onChange={(e) => setSelection(e.target.value)}
            className="w-2/3 p-3 text-black text-lg rounded-md"
          >
            <option value="" disabled>
              Select
            </option>
            {options.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        {/* Message and Action */}
        <div className='bg-accent-light p-4'>
        <div className=" p-4 rounded-md">
          <p className="text-white mb-2">The coupon is currently empty</p>
          <p className="text-white">
            Close Betslip and click on the odds to add your selections
          </p>
        </div>

        {/* <div className="flex justify-center my-4">
          <button className="bg-lime-600 p-2 rounded-full">
            <span className="text-black">&#9650;</span> 
          </button>
        </div> */}

        {/* Continue Button */}
        <div className="flex justify-end mt-2">
          <button className="bg-lime-600 text-white px-6 py-2 rounded-lg hover:bg-lime-700">
            CONTINUE BETTING
          </button>
        </div>

        </div>

        

      </div>
    </div>
  );
};

export default QuickBet;
