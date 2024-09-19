import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GiSoccerBall } from 'react-icons/gi';
import { FaTv } from 'react-icons/fa';
import { AiOutlineLock } from 'react-icons/ai';

const games = ['Soccer', 'Basketball', 'Baseball', 'Tennis'];
const betType = ['1X2', 'Next Goal', 'Over/Under', 'GG/NG'];
const matches = [
  {
    id: 1,
    league: 'Ecuador - Copa Ecuador',
    time: '1st half 45:08',
    team_1: { name: 'CS Emelec', score: 0 },
    team_2: { name: 'CD Tecnico Universitario', score: 0 },
    odds: { home: '1', draw: 'X', away: '2' },
  },
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
    navigate(`/live-stream/${matchId}`);
  };

  return (
    <section className="bg-accent-dark text-white">
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
      <div className="flex flex-wrap justify-between w-full p-4 bg-black gap-2 sm:gap-4">
        {betType.map((type) => (
          <div
            key={type}
            onClick={() => handleBetType(type)}
            className={`text-white flex-1 min-w-[70px] text-center p-1 sm:p-2 ${
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
            className="bg-accent-dark p-4 rounded shadow cursor-pointer"
          >
            {/* League and Time */}
            <div className="flex justify-between items-center">
              <p className="font-bold">{match.league}</p>
              <div className="flex items-center gap-2">
                <span className="bg-green-600 px-2 py-1 rounded-full text-xs sm:text-sm flex items-center justify-center min-w-[60px]">
                  {match.time}
                </span>
                <FaTv className="text-white" />
              </div>
            </div>

            {/* Teams and Scores */}
            <div className="flex justify-between my-4">
              <div className="flex flex-col">
                <span>{match.team_1.name}</span>
                <span>{match.team_2.name}</span>
              </div>
              <div className="flex flex-col text-right">
                <span>{match.team_1.score}</span>
                <span>{match.team_2.score}</span>
              </div>
            </div>

            {/* Odds */}
            <div className="flex justify-between mt-2 gap-1">
              <span className="px-6 py-2 rounded-l-md w-1/3 ring-1 ring-white text-white text-center flex items-center justify-center">
                {match.odds.home}
                <AiOutlineLock className="ml-2" />
              </span>
              <span className="px-6 py-2 w-1/3 ring-1 ring-white text-white text-center">
                {match.odds.draw}
              </span>
              <span className="px-6 py-2 rounded-r-md w-1/3 ring-1 ring-white text-white text-center flex items-center justify-center">
                {match.odds.away}
                <AiOutlineLock className="ml-2" />
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
      <div className="text-center bg-primary py-2 border-b-2 text-accent-dark border-b-white rounded-t-md mt-4">
        Popular
      </div>
      <div className="rounded-2xl mx-4 mt-4 p-2 bg-primary w-12">
        <GiSoccerBall className="text-2xl cursor-pointer" />
      </div>
    </section>
  );
};

export default LiveMatches;
