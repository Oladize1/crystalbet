import React from 'react';
import { useParams } from 'react-router-dom';

// Example match data for simplicity; replace with your data fetching logic if needed
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

const LiveMatchStream = () => {
  const { matchId } = useParams(); // Extract match ID from the URL
  const match = matches.find((m) => m.id === parseInt(matchId)); // Find match by ID

  if (!match) {
    return <div className="text-white">Match not found.</div>;
  }

  return (
    <section className="p-4">
      <header className="flex justify-between items-center bg-primary p-4">
        <h1 className="text-lg font-bold text-white">{match.league}</h1>
        <div className="flex items-center gap-4">
          <span className="text-green-500">{match.time}</span>
          <div className="text-white">
            {match.team_1.name} {match.team_1.score} - {match.team_2.score} {match.team_2.name}
          </div>
        </div>
      </header>
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
      {/* Add additional match details here, styled according to your requirements */}
    </section>
  );
};

export default LiveMatchStream;
