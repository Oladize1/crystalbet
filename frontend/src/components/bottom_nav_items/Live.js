import React, { useState } from 'react';

const sports = [
  { name: 'Soccer', count: 13, icon: '⚽', active: true },
  { name: 'Basketball', count: 7, icon: '🏀' },
  { name: 'Baseball', count: 8, icon: '⚾' },
  { name: 'Tennis', count: 8, icon: '🎾' },
  { name: 'Football', count: 3, icon: '🏈' },
  { name: 'Volleyball', count: 18, icon: '🏐' },
];

const filters = [
  { name: 'All', active: true },
  { name: 'Germany Amateur', flag: '🇩🇪' },
  { name: 'Colombia', flag: '🇨🇴' },
  { name: 'International' },
  { name: 'Mexico', flag: '🇲🇽' },
  { name: 'Argentina', flag: '🇦🇷' },
  { name: 'Brazil', flag: '🇧🇷' },
  { name: 'Australia', flag: '🇦🇺' },
  { name: 'USA', flag: '🇺🇸' },
];

const matches = [
  {
    sport: 'Soccer',
    league: 'GERMANY AMATEUR - BREMEN-LIGA',
    country: 'Germany Amateur',
    flag: '🇩🇪',
    matches: [
      {
        time: '2nd half 61:08',
        teams: ['SC Vahr Blockdiek', 'ESC Geestemunde'],
        score: ['1', '0'],
        ft: ['0', '0'],
        h1: ['0', '0'],
        h2: ['1', '0'],
      },
    ],
  },
  {
    sport: 'Soccer',
    league: 'COLOMBIA - PRIMERA B',
    country: 'Colombia',
    flag: '🇨🇴',
    matches: [
      {
        time: '1st half 15:35',
        teams: ['Real Soacha Cundinamarca', 'Llaneros FC'],
        score: ['0', '0'],
        ft: ['0', '0'],
        h1: ['0', '0'],
        h2: ['0', '0'],
      },
    ],
  },
  // Other sports and matches...
];

const LivePage = () => {
  const [selectedSport, setSelectedSport] = useState('Soccer');
  const [selectedFilter, setSelectedFilter] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');

  // Filter matches based on selected sport, filter (country), and search term
  const filteredMatches = matches.filter(
    (match) =>
      match.sport === selectedSport &&
      (selectedFilter === 'All' || match.country === selectedFilter) &&
      match.matches.some((m) =>
        m.teams.join(' ').toLowerCase().includes(searchTerm.toLowerCase())
      )
  );

  return (
    <div className="bg-accent text-white min-h-screen mt-16 mb-20">
      {/* Header */}
      <div className="bg-primary-dark p-2 flex items-center">
        <span className="text-sm font-semibold">◀ Live In Play</span>
      </div>

      {/* Sports Navigation */}
      <div className="flex space-x-4 p-1 bg-accent-dark">
        {sports.map((sport, index) => (
          <div
            key={index}
            onClick={() => setSelectedSport(sport.name)}
            className={`flex flex-col items-center justify-center py-2 px-5 text-center rounded-lg cursor-pointer w-24 h-24 ${
              selectedSport === sport.name ? 'bg-primary-dark text-black font-bold' : 'bg-accent-dark text-secondary-light'
            }`}
          >
            <span className="text-xs top-2 pl-10">{sport.count}</span>
            <span>{sport.icon}</span>
            <span className="text-sm">{sport.name}</span>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-2 p-4">
        {filters.map((filter, index) => (
          <button
            key={index}
            onClick={() => setSelectedFilter(filter.name)}
            className={`flex items-center px-4 py-2 text-sm rounded-md cursor-pointer ${
              selectedFilter === filter.name ? 'bg-primary-dark' : 'bg-accent-dark text-secondary-light'
            }`}
          >
            {filter.flag && <span className="mr-1">{filter.flag}</span>}
            {filter.name}
          </button>
        ))}
      </div>

      {/* Search Bar and Dropdown */}
      <div className="flex items-center px-2 py-1">
        <input
          type="text"
          placeholder="Filter events in this section by name"
          className="w-1/2 px-3 py-1 mr-2 text-black bg-white rounded-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select
          className="w-1/2 px-3 py-1 ml-2 text-black bg-white rounded-md"
          defaultValue="1x2"
        >
          <option value="1x2">1x2</option>
          <option value="Over/Under">Over/Under</option>
          <option value="Both Teams to Score">Both Teams to Score</option>
        </select>
      </div>

      {/* Matches */}
      <div className="p-2 space-y-6">
        {filteredMatches.length > 0 ? (
          filteredMatches.map((league, index) => (
            <div key={index}>
              <div className="flex items-center justify-between p-2 bg-primary-dark rounded-md">
                <span className="flex items-center gap-2">
                  {league.flag && <span>{league.flag}</span>}
                  {league.league}
                </span>
              </div>
              {league.matches.map((match, matchIndex) => (
                <div
                  key={matchIndex}
                  className="flex flex-col p-4 mt-2 bg-accent-dark rounded-md"
                >
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span className="bg-primary-dark px-2 py-1 rounded">
                      {match.time}
                    </span>
                    <div className="flex space-x-4">
                      <span>FT: {match.ft.join('-')}</span>
                      <span>1H: {match.h1.join('-')}</span>
                      <span>2H: {match.h2.join('-')}</span>
                    </div>
                  </div>
                  <div className="flex flex-col mt-2">
                    {match.teams.map((team, teamIndex) => (
                      <span key={teamIndex} className="py-1">
                        {team}
                      </span>
                    ))}
                  </div>
                  <div className="flex mt-4 space-x-4">
                    <button className="flex-1 py-2 bg-gray-800 rounded text-center">
                      1
                    </button>
                    <button className="flex-1 py-2 bg-gray-800 rounded text-center">
                      X
                    </button>
                    <button className="flex-1 py-2 bg-gray-800 rounded text-center">
                      2
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ))
        ) : (
          <p className="text-center text-gray-400">
            No matches available for the selected sport and filter.
          </p>
        )}
      </div>
    </div>
  );
};

export default LivePage;
