import React from 'react';
import { LuLineChart } from "react-icons/lu";

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
      <div className="flex space-x-2 overflow-x-scroll scrollbar-hide w-full pb-2">
      <div className="flex items-center text-sm px-5 py-3 bg-primary rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Internazionali di Club - Champions League
      </div>
      <div className="flex items-center text-sm px-5 py-3 text-accent bg-secondary rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Internazionali di Club - Europa League
      </div>
      <div className="flex items-center text-sm w-48 px-4 py-1 bg-secondary text-accent rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Svezia - Allsvenskan
      </div>
      <div className="flex items-center text-sm w-48 px-4 py-1 bg-secondary text-accent rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Finlandia - Veikkausliiga
      </div>
      <div className="flex items-center text-sm px-4 py-1 bg-secondary text-accent rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Norvegia - Eliteserien
      </div>
      <div className="flex items-center text-sm px-4 py-1 bg-secondary text-accent rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Brasileiro - Brasileiro Seria A
      </div>
      <div className="flex items-center text-sm w-48 px-4 py-1 bg-secondary text-accent rounded-full whitespace-nowrap">
        <span className="mr-1">⚽</span>
        Stati Uniti - MLS
      </div>
    </div>
      <div className="flex gap-2 mb-4">
        <button className="bg-primary text-accent px-4 py-2 rounded-full">1x2</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">DC</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">Over/Under 2.5</button>
        <button className="bg-white text-black px-4 py-2 rounded-full">GG/NG</button>
      </div>
      {/* Match List */}
      <div>
        <h5 className="text-lg font-bold mb-2">Internazionali di Club - Champions League</h5>
        {matches.map((match, index) => (
          <div key={index} className="flex justify-between items-center p-2  mb-2 rounded-lg">
            <div className="flex flex-col">
              <div className='flex justify-center items-center gap-2'>
                <LuLineChart size={24}/>
              <div className="bg-primary text-accent px-2 py-1 rounded-full">
                {match.id}
              </div>
              <div className="bg-primary rounded-full px-4 py-2 text-sm text-accent font-light">
                {match.time}
              </div>
              </div>
              <div>
                <div>{match.team1}</div>
                <div>{match.team2}</div>
              </div>
            </div>
            <div className="flex space-x-2">
              {match.odds.map((odd, i) => (
                <button key={i} className="px-6 py-2 rounded-md w-1/3 ring-1 ring-white text-white">
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
