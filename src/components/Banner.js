import React from 'react';
import backgroundImage from '../assets/banner-bg.jpg';

const Banner = ({ title, team1, time, team2, odds }) => (
  <section 
    className="bg-cover bg-center text-white text-center py-10"
    style={{ backgroundImage: `url(${backgroundImage})` }}
  >
    <p className="text-2xl font-bold mb-4">{title}</p>
    <div>
      <div className='flex justify-between space-x-8 mx-auto my-6 w-9/12'>
        <div>{team1}</div>
        <div>{time}</div>
        <div>{team2}</div>
      </div>
      <div className="flex justify-center space-x-2 mx-2">
        {odds.map((odd, index) => (
          <button
            key={index}
            className={`px-6 py-2 ${index === 0 ? 'rounded-l-md' : ''} ${index === odds.length - 1 ? 'rounded-r-md' : ''} w-1/3 ring-1 ring-white`}
          >
            {odd}
          </button>
        ))}
      </div> 
    </div>
  </section>
);

export default Banner;
