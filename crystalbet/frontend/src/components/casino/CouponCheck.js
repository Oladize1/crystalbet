import React from 'react';
import { FaArrowLeft } from 'react-icons/fa';

const CouponCheck = () => {
  return (
    <div className="bg-accent-dark mt-24 p-4">
      <div className="flex items-center text-primary cursor-pointer">
        <button onClick={() => window.history.back()} className="flex items-center gap-2">
         <FaArrowLeft/>
        <h1 className="text-xl">Coupon Check</h1>
        </button>
      </div>
      <div className="mt-4">
        <p className="text-gray-300">
          Insert a coupon code to check the status of your bet.
        </p>
        <div className="mt-2">
          <input
            type="text"
            placeholder="Input your coupon code"
            className="w-full p-2 text-gray-800 bg-gray-300 rounded-md focus:outline-none"
          />
        </div>
        <button className="mt-4 bg-primary text-secondary py-2 px-4 rounded-md hover:bg-green-600">
          CHECK
        </button>
      </div>
    </div>
  );
};

export default CouponCheck;
