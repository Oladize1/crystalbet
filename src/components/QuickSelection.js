import React from 'react';

const matches = [
  {
    id: 1366,
    time: "30 Lug - 18:00",
    team1: "Qarabag FK",
    team2: "Lincoln Red Imps",
    odds: ["1.08", "9.00", "18"]
  },
  {
    id: 1136,
    time: "30 Lug - 19:00",
    team1: "Fenerbahce Istanbul",
    team2: "FC Lugano",
    odds: ["1.29", "5.25", "8.00"]
  },
  {
    id: 1478,
    time: "30 Lug - 19:00",
    team1: "Sparta Prague",
    team2: "Shamrock Rovers",
    odds: ["1.15", "7.00", "13"]
  },
  {
    id: 1073,
    time: "30 Lug - 19:00",
    team1: "Petrocub Hincesti",
    team2: "APOEL Nicosia",
    odds: ["2.65", "3.10", "2.56"]
  }
];

const BettingComponent = () => {
  return (
    <div className="bg-black text-white p-4 ">
      {/* Navigation buttons */}
      <div className="flex gap-2 mb-4">
        <button className="bg-green-500 text-black px-4 py-2 rounded-full">1x2</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">DC</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">Over/Under 2.5</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">GG/NG</button>
      </div>
      {/* Match List */}
      <div>
        <h5 className="text-lg font-bold mb-2">Internazionali di Club - Champions League</h5>
        {matches.map((match, index) => (
          <div key={index} className="flex justify-between items-center p-2 bg-gray-900 mb-2 rounded-lg">
            <div className="flex items-center">
              <div className="bg-green-500 text-white px-2 py-1 rounded-lg mr-2">
                {match.id}
              </div>
              <div className="text-gray-400 mr-4">
                {match.time}
              </div>
              <div>
                <div>{match.team1}</div>
                <div>{match.team2}</div>
              </div>
            </div>
            <div className="flex space-x-2">
              {match.odds.map((odd, i) => (
                <button key={i} className="bg-gray-700 text-white px-4 py-2 rounded-lg">
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
