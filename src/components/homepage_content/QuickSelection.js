import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LuLineChart } from 'react-icons/lu';

// League and betting type data
const leagues = [
  "Italy - Serie A",
  "England - Premier League",
  "Germany - Bundesliga",
  "France - Ligue 1",
  "Spain - LaLiga",
  "Netherlands - Eredivisie"
];

const bettingTypes = [
  "1x2",
  "Double Chance",
  "Over/Under 2.5",
  "GG/NG"
];

// Match data with odds for each betting type
const matches = [
  {
    id: 1035,
    team1: "Como 1907",
    team2: "Bologna",
    time: "14 Sep - 15:00",
    league: "Italy - Serie A",
    odds: {
      "1x2": ["2.77", "3.25", "2.62"],
      "Over/Under 2.5": ["2.11", "1.66"],
      "Double Chance": ["1.45", "2.00"],
      "GG/NG": ["1.80", "1.95"]
    }
  },
  {
    id: 1165,
    team1: "Empoli",
    team2: "Juventus",
    time: "14 Sep - 18:00",
    league: "Italy - Serie A",
    odds: {
      "1x2": ["4.75", "3.65", "1.75"],
      "Over/Under 2.5": ["2.07", "1.68"],
      "Double Chance": ["1.70", "2.10"],
      "GG/NG": ["1.90", "1.85"]
    }
  },
  {
    id: 1178,
    team1: "Milan",
    team2: "Venezia FC",
    time: "14 Sep - 20:45",
    league: "Italy - Serie A",
    odds: {
      "1x2": ["1.30", "5.75", "9.25"],
      "Over/Under 2.5": ["1.49", "2.47"],
      "Double Chance": ["1.10", "3.25"],
      "GG/NG": ["1.85", "1.95"]
    }
  }
];

const BettingComponent = () => {
  const navigate = useNavigate();
  
  // State to handle selected league and betting type
  const [selectedLeague, setSelectedLeague] = useState(leagues[0]);
  const [selectedBettingType, setSelectedBettingType] = useState(bettingTypes[0]);

  // Function to handle match clicks and navigate to match details
  const handleMatchClick = (match) => {
    navigate(`/match/${match.id}`, { state: { match, selectedBettingType } }); // Pass selectedBettingType along with match data
  };

  // Function to get the correct odds based on selected betting type
  const getOddsForBettingType = (match, bettingType) => {
    return match.odds[bettingType] || [];
  };

  // Filter matches based on selected league
  const filteredMatches = matches.filter(
    match => match.league === selectedLeague
  );

  return (
    <div className="bg-accent-dark text-secondary-dark px-2 py-4 w-full">
      {/* League selection buttons */}
      <div className="flex flex-wrap gap-2 mb-4">
        {leagues.map((league, index) => (
          <button
            key={index}
            className={`px-4 py-2 rounded-full ${
              selectedLeague === league ? "bg-primary text-secondary" : "bg-accent"
            }`}
            onClick={() => setSelectedLeague(league)}
          >
            {league}
          </button>
        ))}
      </div>

      {/* Betting type selection buttons */}
      <div className="flex gap-3 mb-4">
        {bettingTypes.map((type, index) => (
          <button
            key={index}
            className={`px-4 py-2 rounded-full ${
              selectedBettingType === type ? "bg-primary-dark text-secondary" : "bg-accent"
            }`}
            onClick={() => setSelectedBettingType(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Display filtered matches */}
      <div className="bg-accent text-secondary-dark rounded-lg p-4">
        <h5 className="text-lg font-bold mb-2">{selectedLeague}</h5>
        {filteredMatches.map((match, index) => (
          <div
            key={index}
            className="flex justify-between items-center p-2 mb-2 rounded-lg cursor-pointer hover:bg-accent-dark"
            onClick={() => handleMatchClick(match)}
          >
            <div className="flex items-center gap-4">
              <div className="flex flex-col items-center">
                <LuLineChart size={24} className="text-primary" />
                <div className="text-accent text-sm mt-1">{match.id}</div>
              </div>
              <div>
                <div className="font-bold">{match.team1}</div>
                <div>{match.team2}</div>
              </div>
            </div>
            <div className="flex space-x-4">
              {getOddsForBettingType(match, selectedBettingType).map((odd, i) => (
                <button key={i} className="px-6 py-2 rounded-md ring-1 ring-secondary text-secondary">
                  {odd}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BettingComponent;
