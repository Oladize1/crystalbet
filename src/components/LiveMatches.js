import React, {useState} from 'react';
// import { Link } from 'react-router-dom';

const games = ['Soccer', 'Basketball', 'Baseball', 'Tennis']
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

const LiveMatches = () => {
  const [activeLink, setActiveLink] = useState('')

const handleClick = (category) => {
  setActiveLink(category);
};

return (
  <section className="bg-gray-800">
    <div className="">
      <div className="flex bg-red-700 w-full justify-left items-center">
        <h2 className='font-bold pl-4 px-4 text-black border-r-2 border-r-white'>Live</h2>
        <nav className="flex space-x-4 py-3 px-4  font-semibold">
        {games.map((category) => (
          <a
            href="#"
            key={category}
            onClick={() => handleClick(category)}
            className={`text-gray-900 ${
              activeLink === category ? 'underline decoration-white underline-offset-8' : ''
            }`}
          >
            {category}
          </a>
        ))}
      </nav>
      </div>
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
)
};

export default LiveMatches;
