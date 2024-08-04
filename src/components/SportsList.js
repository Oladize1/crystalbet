import React from 'react';
import { FaBox, FaHandRock, FaFootballBall, FaVolleyballBall, FaWater, FaUserNinja } from 'react-icons/fa';

const sports = [
  { name: "Calcio", icon: "⚽", count: 498 },
  { name: "Basket", icon: "🏀", count: 9 },
  { name: "Baseball", icon: "⚾", count: 31 },
  { name: "Hockey", icon: "🏒", count: 6 },
  { name: "Tennis", icon: "🎾", count: 183 },
  { name: "Pallamano", icon: <FaHandRock />, count: 6 },
  { name: "Pugilato", icon: <FaBox />, count: 18 },
  { name: "Rugby", icon: <FaFootballBall />, count: 14 },
  { name: "Pallavolo", icon: <FaVolleyballBall />, count: 7 },
  { name: "Pallanuoto", icon: <FaWater />, count: 6 },
  { name: "MMA", icon: <FaUserNinja />, count: 3 }
];

const SportsList = () => (
  <section className="py-10 text-white md:w-full">
    <div className="container mx-auto">
      <h2 className="text-2xl font-bold mb-6">Sfoglia gli sport</h2>
      <ul className="">
        {sports.map((sport, index) => (
          <li key={index} className="flex justify-between items-center bg-accent p-4 rounded">
            <div className="flex items-center space-x-2">
              <div className="text-xl">
                {sport.icon}
              </div>
              <div>
                {sport.name}
              </div>
            </div>
            <div className="text-white items-end">
              {sport.count} <span className='pl-1 font-semibold text-lg'>&gt;</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  </section>
  // <div className="bg-gray-800 text-white min-h-screen p-4">
  //     {/* Top navigation */}
      

  //     {/* Betting options */}
  //     <div className="flex space-x-4 my-4">
  //       <button className="px-4 py-2 bg-green-500 rounded-full">1x2</button>
  //       <button className="px-4 py-2 bg-gray-700 rounded-full">DC</button>
  //       <button className="px-4 py-2 bg-gray-700 rounded-full">Over/Under 2.5</button>
  //       <button className="px-4 py-2 bg-gray-700 rounded-full">GG/NG</button>
  //     </div>

  //     {/* Match list */}
  //     <div className="bg-gray-900 p-4 rounded-lg">
  //       <div className="mb-4">
  //         <div className="flex items-center space-x-4">
  //           <span className="bg-gray-700 px-2 py-1 rounded">1149</span>
  //           <span>06 Ago - 18:00</span>
  //           <span>Qarabag FK vs PFC Ludogorets 1945 Razgrad</span>
  //         </div>
  //         <div className="flex space-x-4 mt-2">
  //           <button className="bg-gray-700 px-4 py-2 rounded">1.71</button>
  //           <button className="bg-gray-700 px-4 py-2 rounded">3.60</button>
  //           <button className="bg-gray-700 px-4 py-2 rounded">4.50</button>
  //         </div>
  //       </div>
  //       <div className="mb-4">
  //         <div className="flex items-center space-x-4">
  //           <span className="bg-gray-700 px-2 py-1 rounded">1156</span>
  //           <span>06 Ago - 19:00</span>
  //           <span>Malmo FF vs PAOK Thessaloniki</span>
  //         </div>
  //         <div className="flex space-x-4 mt-2">
  //           <button className="bg-gray-700 px-4 py-2 rounded">2.38</button>
  //           <button className="bg-gray-700 px-4 py-2 rounded">3.30</button>
  //           <button className="bg-gray-700 px-4 py-2 rounded">2.80</button>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
);

export default SportsList;
