import React from 'react';
import { useNavigate } from 'react-router-dom';

const BookABet = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center mt-16">
      {/* Title section */}
      <div className="w-full bg-primary-dark py-4">
        <div className="text-left pl-4">
          <button className="text-black font-bold" onClick={() => navigate(-1)}>
          ◀ Book A Bet
          </button>
        </div>
      </div>

      {/* Input Section */}
      <div className="w-full bg-accent-dark p-6 mt-2 rounded-md">
        <p className="text-white mb-4 text-center">
          Insert a booking code to add the selections to your bet slip:
        </p>
        <input
          type="text"
          placeholder="E.G. 1XBGHH"
          className="w-full p-3 text-black text-lg rounded-md placeholder-gray-500"
        />

        {/* Buttons */}
        <div className="flex justify-between mt-6">
          <button
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
            onClick={() => navigate(-1)} // Assuming cancel should go back
          >
            CANCEL
          </button>
          <button className="bg-lime-600 text-white px-6 py-2 rounded-lg hover:bg-lime-700">
            PROCEED
          </button>
        </div>
      </div>
    </div>
  );
};

export default BookABet;
