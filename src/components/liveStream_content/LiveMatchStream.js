import React from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Add useNavigate for the back button

// Example match data for simplicity; replace with your data fetching logic if needed
const matches = [
  {
    id: 1,
    league: 'Brazil - Brasileiro Serie A',
    teams: 'Fluminense FC RJ vs SE Palmeiras SP',
    time: '2nd half 71:47',
    team_1: { name: 'Fluminense FC RJ', score: 0, yellowCards: 1, redCards: 0 },
    team_2: { name: 'SE Palmeiras SP', score: 0, yellowCards: 1, redCards: 2 },
    odds: { home: '4.55', draw: '1.55', away: '4.60' },
  },
  // Add more matches as needed
];

const LiveMatchStream = () => {
  const { matchId } = useParams(); // Extract match ID from the URL
  const navigate = useNavigate();  // Hook for navigation
  const match = matches.find((m) => m.id === parseInt(matchId)); // Find match by ID

  if (!match) {
    return <div className="text-white">Match not found.</div>;
  }

  return (
    <section className="p-2 my-16">
      {/* Header */}
      <header className="flex justify-between items-center bg-primary-dark p-4">
        <button 
          onClick={() => navigate(-1)} // Go back to the previous page
          className="text-white text-xl"
        >
          {'<'} Back to Matches
        </button>
        <h1 className="text-lg font-bold text-white">{match.league}</h1>
      </header>

      {/* Match Info */}
      <div className="bg-accent-dark text-white py-4 px-6">
        <div className="flex justify-between items-center">
          {/* Time */}
          <div className="flex items-center gap-2">
            <span className="text-primary-dark px-2 py-1 bg-black rounded">
              {match.time}
            </span>
          </div>
        </div>

        <div className="flex justify-between py-4">
          {/* Team 1 */}
          <div className="flex flex-col items-center">
            <span className="font-semibold">{match.team_1.name}</span>
            <span className="text-4xl font-bold">{match.team_1.score}</span>
            <div className="flex gap-2">
              <span className="text-yellow-400">🟨 {match.team_1.yellowCards}</span>
              <span className="text-red-600">🟥 {match.team_1.redCards}</span>
            </div>
          </div>

          {/* Versus Divider */}
          <div className="flex flex-col items-center justify-center">
            <span className="text-xl">VS</span>
          </div>

          {/* Team 2 */}
          <div className="flex flex-col items-center">
            <span className="font-semibold">{match.team_2.name}</span>
            <span className="text-4xl font-bold">{match.team_2.score}</span>
            <div className="flex gap-2">
              <span className="text-yellow-400">🟨 {match.team_2.yellowCards}</span>
              <span className="text-red-600">🟥 {match.team_2.redCards}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Odds */}
      <div className="flex justify-center mt-2 gap-1">
        <span className="px-6 py-2 rounded-l-md w-1/3 ring-1 ring-white text-white text-center">
          {match.odds.home}
        </span>
        <span className="px-6 py-2 w-1/3 ring-1 ring-white text-white text-center">
          {match.odds.draw}
        </span>
        <span className="px-6 py-2 rounded-r-md w-1/3 ring-1 ring-white text-white text-center">
          {match.odds.away}
        </span>
      </div>
    </section>
  );
};

export default LiveMatchStream;
