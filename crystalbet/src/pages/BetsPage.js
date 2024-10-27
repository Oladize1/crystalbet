import React, { useState, useEffect } from 'react';
import TopNav from '../components/homepage_content/TopNav';
import AutoScrollCarousel from '../components/AutoScrollCarousel';
import LiveMatches from '../components/homepage_content/LiveMatches';
import QuickSelection from '../components/homepage_content/QuickSelection';
import SportLists from '../components/homepage_content/SportsList';
import BetHistory from '../components/BetHistory';
import Spinner from '../components/PreLoader';

// Import the API methods from api.js
import { fetchLiveBets, fetchVirtualGames, fetchBetHistory } from '../services/api'; // Adjust path if necessary

const HomePage = () => {
  const [globalLoading, setGlobalLoading] = useState(true);
  const [liveMatches, setLiveMatches] = useState([]);
  const [sportsCategories, setSportsCategories] = useState([]);
  const [betHistory, setBetHistory] = useState([]);
  const [error, setError] = useState(null);

  const user = true; // Simulate user logged in

  // Fetch live matches from the backend
  const loadLiveMatches = async () => {
    try {
      const { data } = await fetchLiveBets(); // Updated to call the API method from api.js
      setLiveMatches(data);
    } catch (err) {
      setError('Failed to load live matches');
    }
  };

  // Fetch sports categories from the backend
  const loadSportsCategories = async () => {
    try {
      const { data } = await fetchVirtualGames(); // Updated to call the API method from api.js
      setSportsCategories(data);
    } catch (err) {
      setError('Failed to load sports categories');
    }
  };

  // Fetch user's bet history from the backend
  const loadBetHistory = async () => {
    try {
      const { data } = await fetchBetHistory(); // Updated to call the API method from api.js
      setBetHistory(data);
    } catch (err) {
      setError('Failed to load bet history');
    }
  };

  useEffect(() => {
    // Simulate loading all data asynchronously
    const loadData = async () => {
      try {
        await Promise.all([
          loadLiveMatches(),
          loadSportsCategories(),
          loadBetHistory(),
        ]);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setGlobalLoading(false);
      }
    };
    
    loadData();
  }, []);

  if (globalLoading) {
    return <Spinner />;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-accent w-full">
      <TopNav />
      <div className="w-full overflow-hidden">
        <AutoScrollCarousel />
      </div>
      <main className="px sm:px-4 lg:px-6 w-full overflow-hidden">
        <LiveMatches matches={liveMatches} />
        <QuickSelection />
        <SportLists sports={sportsCategories} />
        {user && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            <BetHistory betHistory={betHistory} />
          </section>
        )}
      </main>
    </div>
  );
};

export default HomePage;
