import React from 'react';
import { FaBox, FaBaseballBall, FaHockeyPuck, FaTableTennis, FaHandRock, FaFootballBall, FaVolleyballBall, FaWater, FaUserNinja } from 'react-icons/fa';

const sports = [
  { name: "Calcio", icon: <FaBox />, count: 498 },
  { name: "Basket", icon: <FaBox />, count: 9 },
  { name: "Baseball", icon: <FaBaseballBall />, count: 31 },
  { name: "Hockey", icon: <FaHockeyPuck />, count: 6 },
  { name: "Tennis", icon: <FaTableTennis />, count: 183 },
  { name: "Pallamano", icon: <FaHandRock />, count: 6 },
  { name: "Pugilato", icon: <FaBox />, count: 18 },
  { name: "Rugby", icon: <FaFootballBall />, count: 14 },
  { name: "Pallavolo", icon: <FaVolleyballBall />, count: 7 },
  { name: "Pallanuoto", icon: <FaWater />, count: 6 },
  { name: "MMA", icon: <FaUserNinja />, count: 3 }
];

const SportsList = () => (
  <section className="py-10 bg-gray-800 text-white">
    <div className="container mx-auto">
      <h2 className="text-2xl font-bold mb-6">Sfoglia gli sport</h2>
      <ul className="space-y-1">
        {sports.map((sport, index) => (
          <li key={index} className="flex justify-between items-center bg-gray-700 p-4 rounded">
            <div className="flex items-center space-x-2">
              <div className="text-xl">
                {sport.icon}
              </div>
              <div>
                {sport.name}
              </div>
            </div>
            <div className="text-white">
              {sport.count} <span className='pl-1 font-semibold text-lg'>&gt;</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  </section>
);

export default SportsList;
