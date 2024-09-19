import React, { useState, useEffect } from 'react';
import TopNav from '../components/homepage_content/TopNav';
import AutoScrollCarousel from '../components/AutoScrollCarousel';
import LiveMatches from '../components/homepage_content/LiveMatches';
import QuickSelection from '../components/homepage_content/QuickSelection';
import SportLists from '../components/homepage_content/SportsList';
import BetHistory from '../components/BetHistory';
import Spinner from '../components/PreLoader'; 

const HomePage = () => {
  const [authLoading, setAuthLoading] = useState(true);
  const [betsLoading, setBetsLoading] = useState(true);
  const [globalLoading, setGlobalLoading] = useState(true);

  const user = true; // Simulate user logged in

  useEffect(() => {
    // Simulate loading with timeout
    const timer = setTimeout(() => {
      setAuthLoading(false);
      setBetsLoading(false);
      setGlobalLoading(false);
      console.log('Loading finished');
    }, 2000); // Simulating 2 seconds delay

    return () => clearTimeout(timer); // Cleanup timer
  }, []);

  // Debug to check if loading state is triggering
  console.log({ authLoading, betsLoading, globalLoading });

  if (globalLoading || authLoading || betsLoading) {
    console.log('Displaying Spinner');
    return <Spinner />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-accent w-full">
      <TopNav />
      <div className="w-full overflow-hidden">
        <AutoScrollCarousel />
      </div>
      <main className="px-4 sm:px-6 lg:px-8 w-full overflow-hidden">
        <LiveMatches />
        <QuickSelection />
        <SportLists />
        {user && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            <BetHistory betHistory={[]} />
          </section>
        )}
      </main>
    </div>
  );
};

export default HomePage;
