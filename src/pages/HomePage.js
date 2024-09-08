import React, { useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { BetContext } from '../context/BetContext';
import Header from '../components/Header';
import TopNav from '../components/homepage_content/TopNav';
import Navbar from '../components/Navbar';
import AutoScrollCarousel from '../components/AutoScrollCarousel'
//import BetList from '../components/BetList';
import LiveMatches from '../components/homepage_content/LiveMatches'
import QuickSelection from '../components/homepage_content/QuickSelection'
import SportLists from '../components/homepage_content/SportsList'
import BetHistory from '../components/BetHistory';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';

const HomePage = () => {
  const { user, loading: authLoading } = useContext(AuthContext);
  const { loading: betsLoading, fetchBetHistory, betHistory } = useContext(BetContext);

  useEffect(() => {
    if (user) {
      fetchBetHistory();
    }
  }, [user, fetchBetHistory]);

  if (authLoading || betsLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-accent w-full">
      <Header />
      <TopNav />
      {/* please change this carousel, i couldn't find better one online */}
      <AutoScrollCarousel />
      <main className="px-4 sm:px-6 lg:px-[0px] w-full">
        <LiveMatches />
        <QuickSelection />
        <SportLists />
        {user && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            <BetHistory betHistory={betHistory} />
          </section>
        )}
      </main>
      <Footer />
      <BackToTop />
      <Navbar />
    </div>
  );
};

export default HomePage;
