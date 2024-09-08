import React from 'react';
import { FaBox, FaHandRock, FaFootballBall, FaVolleyballBall, FaWater, FaUserNinja } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const sports = [
  { name: "Football", icon: "⚽", count: 498, path: "football" },
  { name: "Basketball", icon: "🏀", count: 9, path: "basketball" },
  { name: "Baseball", icon: "⚾", count: 31, path: "baseball" },
  { name: "Hockey", icon: "🏒", count: 6, path: "hockey" },
  { name: "Tennis", icon: "🎾", count: 183, path: "tennis" },
  { name: "Handball", icon: <FaHandRock />, count: 6, path: "handball" },
  { name: "Boxing", icon: <FaBox />, count: 18, path: "boxing" },
  { name: "Rugby", icon: <FaFootballBall />, count: 14, path: "rugby" },
  { name: "Volleyball", icon: <FaVolleyballBall />, count: 7, path: "volleyball" },
  { name: "Water Polo", icon: <FaWater />, count: 6, path: "water-polo" },
  { name: "MMA", icon: <FaUserNinja />, count: 3, path: "mma" }
];

const SportsList = () => {
  const navigate = useNavigate();

  const handleSportClick = (path) => {
    navigate(`/sports/${path}`);
  };

  return (
    <section className="py-10 text-white w-full">
      <div className="mx-2">
        <h2 className="text-2xl font-bold mb-6">Browse Sports</h2>
        <ul className="space-y-4">
          {sports.map((sport, index) => (
            <li 
              key={index} 
              className="flex justify-between items-center bg-accent p-4 rounded cursor-pointer hover:bg-accent-dark"
              onClick={() => handleSportClick(sport.path)}
            >
              <div className="flex items-center space-x-2">
                <div className="text-xl">
                  {sport.icon}
                </div>
                <div className="text-sm sm:text-base md:text-lg">
                  {sport.name}
                </div>
              </div>
              <div className="text-white text-sm sm:text-base md:text-lg">
                {sport.count} <span className='pl-1 font-semibold'>&gt;</span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};

export default SportsList;
