import React, { useState } from 'react';
import { Link } from 'react-router-dom'
import { FaFootballBall, FaHandRock, FaBasketballBall, FaBaseballBall, FaHockeyPuck, FaStar } from 'react-icons/fa';

const sports = [
  { name: "Soccer", icon: <FaFootballBall />, id: 'soccer' },
  { name: "Tennis", icon: <FaHandRock />, id: 'tennis' },
  { name: "Basketball", icon: <FaBasketballBall />, id: 'basketball' },
  { name: "All Sports", icon: <FaStar />, id: 'all' }  // Updated this line
];

const allSportsList = [
  { name: "Calcio", icon: <FaFootballBall />, count: 733, id: 'soccer' },
  { name: "Basket", icon: <FaBasketballBall />, count: 17, id: 'basketball' },
  { name: "Baseball", icon: <FaBaseballBall />, count: 27, id: 'baseball' },
  { name: "Hockey", icon: <FaHockeyPuck />, count: 27, id: 'hockey' },
  { name: "Tennis", icon: <FaHandRock />, count: 28, id: 'tennis' },
  { name: "Pallamano", icon: <FaHandRock />, count: 49, id: 'pallamano' }
];

const sportDetails = {
  soccer: [
    { name: "INTERNATIONALI", count: 34 },
    { name: "INTERNATIONALI DI CLUB", count: 46 },
    { name: "ITALIA", count: 49 },
    { name: "INGHILTERRA", count: 47 },
    { name: "GERMANIA", count: 18 }
  ],
  tennis: [
    { name: "Wimbledon", count: 15 },
    { name: "US Open", count: 12 },
    { name: "French Open", count: 14 }
  ],
  basketball: [
    { name: "NBA", count: 30 },
    { name: "EuroLeague", count: 20 },
    { name: "FIBA", count: 10 }
  ]
};

const SportsPage = () => {
  const [selectedSport, setSelectedSport] = useState('soccer');
  const [isAllSportsView, setIsAllSportsView] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [selectedCountry, setSelectedCountry] = useState('all');

  const handleSportClick = (sportId) => {
    setSelectedSport(sportId);
    setIsAllSportsView(false);
  };

  const handleAllSportsClick = () => {
    setIsAllSportsView(true);
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

  const handleCountryChange = (event) => {
    setSelectedCountry(event.target.value);
  };

  const filteredSports = allSportsList.filter(sport =>
    sport.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredDetails = sportDetails[selectedSport]?.filter(detail =>
    selectedCountry === 'all' || detail.name.toLowerCase().includes(selectedCountry.toLowerCase())
  );

  return (
    <div className="text-white min-h-screen my-16">
      {/* Back to Home */}
      <div className="p-4 bg-accent-dark">
        <Link to="/">
        <button className="text-primary-dark">&lt; Back to Home</button>
        </Link>
      </div>

      {/* Top Navigation for Sports */}
      <div className="flex space-x-4 p-4">
        {sports.map((sport) => (
          <button
            key={sport.id}
            onClick={() =>
              sport.id === 'all' ? handleAllSportsClick() : handleSportClick(sport.id)
            }
            className={`flex items-center justify-center w-full px-4 py-8 rounded-lg space-x-2 ${
              selectedSport === sport.id || (isAllSportsView && sport.id === 'all') ? 'bg-primary-dark' : 'bg-accent-dark'
            }`}
          >
            <span>{sport.icon}</span>
            <span>{sport.name}</span>
          </button>
        ))}
      </div>

      {/* Filter Buttons */}
      {!isAllSportsView && (
        <div className="p-4">
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => setFilter('allByCountry')}
              className={`px-4 py-2 rounded-full text-left ${filter === 'allByCountry' ? 'bg-primary-dark' : 'bg-accent-dark'}`}
            >
              All By Country
            </button>
            <button
              onClick={() => setFilter('allCompetitions')}
              className={`px-4 py-2 rounded-full text-left ${filter === 'allCompetitions' ? 'bg-primary-dark' : 'bg-accent-dark'}`}
            >
              All Competitions
            </button>
            <button
              onClick={() => setFilter('antepost')}
              className={`px-4 py-2 rounded-full text-left ${filter === 'antepost' ? 'bg-primary-dark' : 'bg-accent-dark'}`}
            >
              Antepost
            </button>
            <div className="relative">
              <select
                value={filter}
                onChange={handleFilterChange}
                className="w-full px-4 py-2 rounded bg-accent-dark text-white appearance-none"
              >
                <option value="allByCountry">All By Country</option>
                <option value="allCompetitions">All Competitions</option>
                <option value="antepost">Antepost</option>
                <option value="all">All</option>
              </select>
            </div>
          </div>

          {/* Country Dropdown for "All By Country" filter */}
          {filter === 'allByCountry' && (
            <div className="mt-4">
              <select
                value={selectedCountry}
                onChange={handleCountryChange}
                className="w-full px-4 py-2 rounded bg-accent-dark text-white"
              >
                <option value="all">All Countries</option>
                <option value="italia">Italia</option>
                <option value="inghilterra">Inghilterra</option>
                <option value="germania">Germania</option>
                {/* Add more options as needed */}
              </select>
            </div>
          )}
        </div>
      )}

      {/* Main Section: All Sports or Sport Specific */}
      <div className="p-4">
        {isAllSportsView ? (
          <>
            {/* Search Bar */}
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Input your search"
              className="w-full px-4 py-2 mb-4 rounded bg-white text-accent"
            />

            {/* Sports List */}
            <ul className="gap-4"> 
              {filteredSports.map((sport, index) => (
                <li
                  key={index}
                  onClick={() => handleSportClick(sport.id)}
                  className="flex justify-between items-center bg-accent-dark p-4 rounded cursor-pointer"
                >
                  <span className="flex items-center space-x-2">
                    <FaStar className="text-yellow-500" />
                    <span className="border-l-2 pl-2 border-gray-600">{sport.name}</span>
                  </span>
                  <span>{sport.count} <span className='pl-1 font-semibold text-lg'>&gt;</span></span>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <>
            <h2 className="text-xl font-bold mb-4">{selectedSport.toUpperCase()}</h2>
            <ul className="space-y-2">
              {filteredDetails?.map((detail, index) => (
                <li
                  key={index}
                  className="flex justify-between items-center bg-accent-dark p-4 rounded"
                >
                  <span>{detail.name}</span>
                  <span>{detail.count} <span className='pl-1 font-semibold text-lg'>&gt;</span></span>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
};

export default SportsPage;
