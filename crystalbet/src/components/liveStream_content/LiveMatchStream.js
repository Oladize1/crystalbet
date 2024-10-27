import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; 

const LiveMatchStream = () => {
  const { matchId } = useParams(); 
  const navigate = useNavigate(); 
  const [match, setMatch] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the match data from the API
    const fetchMatch = async () => {
      try {
        const response = await fetch(`/api/matches/${matchId}`);
        if (!response.ok) {
          throw new Error('Match not found');
        }
        const data = await response.json();
        setMatch(data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchMatch();
  }, [matchId]);

  if (error) {
    return <div className="text-white">{error}</div>;
  }

  if (!match) {
    return <div className="text-white">Loading...</div>;
  }

  return (
    <section className="p-2 my-16">
      <header className="flex justify-between items-center bg-primary-dark p-4">
        <button onClick={() => navigate(-1)} className="text-white text-xl">{'<'} Back to Matches</button>
        <h1 className="text-lg font-bold text-white">{match.league}</h1>
      </header>

      <div className="bg-accent-dark text-white py-4 px-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-primary-dark px-2 py-1 bg-black rounded">{match.time}</span>
          </div>
        </div>

        <div className="flex justify-between py-4">
          <div className="flex flex-col items-center">
            <span className="font-semibold">{match.team_a}</span>
            <span className="text-4xl font-bold">{match.score}</span>
          </div>
          <div className="flex flex-col items-center justify-center">
            <span className="text-xl">VS</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="font-semibold">{match.team_b}</span>
            <span className="text-4xl font-bold">{match.score}</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LiveMatchStream;
