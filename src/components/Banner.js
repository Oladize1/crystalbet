import React from 'react';

const Banner = () => (
  <section className="bg-gray-900 text-white text-center py-10">
    <h1 className="text-3xl font-bold mb-4">Premier League</h1>
    <p className="mb-4">Ipswich Town vs Liverpool FC</p>
    <div className="flex justify-center space-x-2 w-100">
      <button className="bg-gray-800 px-6 py-2 rounded min-w-24">7.25</button>
      <button className="bg-gray-800 px-6 py-2 rounded min-w-24">5.50</button>
      <button className="bg-gray-800 px-6 py-2 rounded min-w-24">1.35</button>
    </div>
  </section>
);

export default Banner;
