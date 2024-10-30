import React, { useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { BetContext } from '../context/BetContext';
import Header from '../components/Header';
import LiveBetList from '../components/LiveBetList';
import Footer from '../components/Footer';

const LiveBetsPage = () => {
  const { loading: authLoading } = useContext(AuthContext);
  const { liveBets, loading: betsLoading, setLiveBets, fetchLiveBets } = useContext(BetContext);

  // Fetch live bets on component mount
  useEffect(() => {
    fetchLiveBets();

    // WebSocket for live updates
    const ws = new WebSocket('ws://localhost:8000/ws/live');

    ws.onmessage = (event) => {
      const updatedLiveBets = JSON.parse(event.data);
      setLiveBets(updatedLiveBets);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    // Clean up WebSocket connection when component unmounts
    return () => {
      ws.close();
    };
  }, [fetchLiveBets, setLiveBets]);

  // Show loading spinner if either auth or bets are still loading
  if (authLoading || betsLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex-1 container mx-auto p-4">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Live Bets</h2>
          <LiveBetList liveBets={liveBets} />
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default LiveBetsPage;
