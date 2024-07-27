import React from 'react';

const Banner = () => (
  <section className="bg-gray-900 text-white text-center py-10">
    <p className="text-2xl font-bold mb-4">Premier League</p>
    <div>
    <div className='flex justify-between space-x-8 mx-auto my-6 w-9/12'>
      <div>
        Ipswich Town 
      </div>
      <div>
        11:30 | 17/07/2024
      </div>
      <div>
        Liverpool FC
      </div>
    </div>
    <div className="flex justify-center space-x-2 mx-2">
      <button className="bg-gray-800 px-6 py-2 rounded-l-md w-1/3 ring-1 ring-white">7.25</button>
      <button className="bg-gray-800 px-6 py-2 w-1/3 ring-1 ring-white">5.50</button>
      <button className="bg-gray-800 px-6 py-2 rounded-r-md w-1/3 ring-1 ring-white">1.35</button>
    </div>
    </div>
  </section>
);

export default Banner;
