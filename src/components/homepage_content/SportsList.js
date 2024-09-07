import React from 'react';
import { FaBox, FaHandRock, FaFootballBall, FaVolleyballBall, FaWater, FaUserNinja } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const sports = [
  { name: "Calcio", icon: "⚽", count: 498, path: "calcio" },
  { name: "Basket", icon: "🏀", count: 9, path: "basket" },
  { name: "Baseball", icon: "⚾", count: 31, path: "baseball" },
  { name: "Hockey", icon: "🏒", count: 6, path: "hockey" },
  { name: "Tennis", icon: "🎾", count: 183, path: "tennis" },
  { name: "Pallamano", icon: <FaHandRock />, count: 6, path: "pallamano" },
  { name: "Pugilato", icon: <FaBox />, count: 18, path: "pugilato" },
  { name: "Rugby", icon: <FaFootballBall />, count: 14, path: "rugby" },
  { name: "Pallavolo", icon: <FaVolleyballBall />, count: 7, path: "pallavolo" },
  { name: "Pallanuoto", icon: <FaWater />, count: 6, path: "pallanuoto" },
  { name: "MMA", icon: <FaUserNinja />, count: 3, path: "mma" }
];

const SportsList = () => {
  const navigate = useNavigate();

  const handleSportClick = (path) => {
    navigate(`/sports/${path}`);
  };

  return (
    <section className="py-10 text-white md:w-full">
      <div className="mx-2">
        <h2 className="text-2xl font-bold mb-6">Sfoglia gli sport</h2>
        <ul>
          {sports.map((sport, index) => (
            <li 
              key={index} 
              className="flex justify-between items-center bg-accent p-4 rounded cursor-pointer"
              onClick={() => handleSportClick(sport.path)}
            >
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
  );
};

export default SportsList;
