import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Badges from './../Badges'; // Ensure the correct path to Badges component
import { GiSoccerBall } from 'react-icons/gi';

const games = ['Soccer', 'Basketball', 'Baseball', 'Tennis'];
const betType = ['1X2', 'Next Goal', 'Over/Under', 'GG/NG'];
const matches = [
  {
    id: 1,
    league: 'Brazil - Brasileiro Serie A',
    teams: 'Fluminense FC RJ vs SE Palmeiras SP',
    time: '2nd half 71:47',
    team_1: { name: 'Fluminense FC RJ', score: 0 },
    team_2: { name: 'SE Palmeiras SP', score: 0 },
    odds: { home: '4.55', draw: '1.55', away: '4.60' },
  },
  {
    id: 2,
    league: 'Brazil - Brasileiro Serie A',
    teams: 'AC Goianiense GO vs EC Bahia BA',
    time: '2nd half 71:47',
    team_1: { name: 'Fluminense FC RJ', score: 1 },
    team_2: { name: 'SE Palmeiras SP', score: 2 },
    odds: { home: '1.27', draw: '4.20', away: '6.50' },
  },
  // Add more matches as needed
];

const LiveMatches = () => {
  const [activeLink, setActiveLink] = useState('');
  const [selectedBetType, setSelectedBetType] = useState('');
  const navigate = useNavigate();

  const handleBetType = (type) => {
    setSelectedBetType(type);
  };

  const handleClick = (category) => {
    setActiveLink(category);
  };

  const handleMatchClick = (matchId) => {
    navigate(`/live-stream/${matchId}`); // Navigate to the live stream page with the match ID
  };

  return (
    <section>
      {/* Games Navigation */}
      <div className="flex bg-primary justify-left items-center w-full">
        <h2 className="font-bold pl-4 px-4 text-black border-r-2 border-r-white">
          Live
        </h2>
        <nav className="flex space-x-4 py-3 px-4 font-semibold">
          {games.map((category) => (
            <button
              key={category}
              onClick={() => handleClick(category)}
              className={`text-gray-900 ${
                activeLink === category ? 'border-b-2' : ''
              }`}
            >
              {category}
            </button>
          ))}
        </nav>
      </div>

      {/* Bet Types */}
      <div className="flex justify-between w-full p-4 bg-black">
        {betType.map((type) => (
          <div
            key={type}
            onClick={() => handleBetType(type)}
            className={`text-white w-1/4 text-center ${
              selectedBetType === type ? 'border-b-4 border-primary' : ''
            }`}
          >
            {type}
          </div>
        ))}
      </div>

      {/* Matches List */}
      <div className="w-full gap-4">
        {matches.map((match) => (
          <div
            key={match.id}
            onClick={() => handleMatchClick(match.id)}
            className="bg-inherit p-4 rounded shadow cursor-pointer"
          >
            <p className="text-white font-bold">{match.league}</p>
            <div className="flex space-x-3">
              <Badges text={match.time} type="Main" />
              <Badges text="TV" type="Sub" />
            </div>
            <div className="flex items-center gap-2 w-full">
              <div>★</div> {/* Replace with a star icon if needed */}
              <div className="flex flex-col">
                <div className="flex justify-between w-full font-semibold text-white">
                  <div>{match.team_1.name}</div>
                  <div className="mr-auto">{match.team_1.score}</div>
                </div>
                <div className="flex items-center justify-between w-full font-semibold text-white">
                  <div>{match.team_2.name}</div>
                  <div className="text-right">{match.team_2.score}</div>
                </div>
              </div>
            </div>
            <div className="flex justify-between mt-2 gap-1">
              <span className="px-6 py-2 rounded-l-md w-1/3 ring-1 ring-white text-white">
                {match.odds.home}
              </span>
              <span className="px-6 py-2 w-1/3 ring-1 ring-white text-white">
                {match.odds.draw}
              </span>
              <span className="px-6 py-2 rounded-r-md w-1/3 ring-1 ring-white text-white">
                {match.odds.away}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* View More Link */}
      <p className="text-white underline font-medium text-right cursor-pointer pr-4">
        View More
      </p>

      {/* Popular Section */}
      <div className="text-center bg-primary py-2 border-b-2 text-gray-800 border-b-white rounded-t-md mt-4">
        Popular
      </div>
      <div className="rounded-2xl mx-4 mt-4 p-2 bg-primary w-12">
        <GiSoccerBall className="text-2xl cursor-pointer" />
      </div>
    </section>
  );
};

export default LiveMatches;