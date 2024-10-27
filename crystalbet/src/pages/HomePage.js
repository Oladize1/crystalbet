import React, { useState, useEffect } from 'react';
import { fetchBetHistory } from '../services/api'; // Import the fetchBetHistory function from api.js
import TopNav from '../components/homepage_content/TopNav';
import AutoScrollCarousel from '../components/AutoScrollCarousel';
import LiveMatches from '../components/homepage_content/LiveMatches';
import QuickSelection from '../components/homepage_content/QuickSelection';
import SportLists from '../components/homepage_content/SportsList';
import BetHistory from '../components/BetHistory';
import Spinner from '../components/PreLoader';

const HomePage = () => {
  const [loading, setLoading] = useState(true);
  const [betHistory, setBetHistory] = useState([]);
  const [error, setError] = useState(null);

  const user = true; // Simulate user logged in

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchBetHistory();
        setBetHistory(response.data.betHistory);
      } catch (error) {
        console.error('Error fetching bet history:', error);
        setError('Failed to load bet history. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Spinner />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-accent w-full">
      <TopNav />
      <div className="w-full overflow-hidden">
        <AutoScrollCarousel />
      </div>
      <main className="px sm:px-4 lg:px-6 w-full overflow-hidden">
        <LiveMatches />
        <QuickSelection />
        <SportLists />
        {user && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            {error && <div className="text-red-500">{error}</div>}
            <BetHistory betHistory={betHistory} />
          </section>
        )}
      </main>
    </div>
  );
};

export default HomePage;
