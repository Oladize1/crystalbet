import React from 'react';

const matches = [
  {
    league: "Brazil - Brasileiro Serie A",
    teams: "Fluminense FC RJ vs SE Palmeiras SP",
    odds: { home: "4.55", draw: "1.55", away: "4.60" }
  },
  {
    league: "Brazil - Brasileiro Serie A",
    teams: "AC Goianiense GO vs EC Bahia BA",
    odds: { home: "1.27", draw: "4.20", away: "6.50" }
  },
  // Add more matches as needed
];

const LiveMatches = () => (
  <section className="py-10 bg-gray-100">
    <div className="container mx-auto">
      <h2 className="text-2xl font-bold mb-6">Live Matches</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {matches.map((match, index) => (
          <div key={index} className="bg-white p-4 rounded shadow">
            <p className="text-gray-600">{match.league}</p>
            <p className="font-bold">{match.teams}</p>
            <div className="flex justify-between mt-2">
              <span>{match.odds.home}</span>
              <span>{match.odds.draw}</span>
              <span>{match.odds.away}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

export default LiveMatches;
