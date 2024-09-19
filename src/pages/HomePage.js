import React, { useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext'; // Authentication context
import { BetContext } from '../context/BetContext'; // Betting context
import Header from '../components/Header';
import TopNav from '../components/homepage_content/TopNav';
import Navbar from '../components/Navbar';
import AutoScrollCarousel from '../components/AutoScrollCarousel';
// import BetList from '../components/BetList'; // (If you need to use the BetList component, you can uncomment this line)
import LiveMatches from '../components/homepage_content/LiveMatches';
import QuickSelection from '../components/homepage_content/QuickSelection';
import SportLists from '../components/homepage_content/SportsList';
import BetHistory from '../components/BetHistory';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';

const HomePage = () => {
  const { user, loading: authLoading } = useContext(AuthContext); // Get user and loading state from AuthContext
  const { loading: betsLoading, fetchBetHistory, betHistory } = useContext(BetContext); // Get loading state, fetch function, and bet history from BetContext

  useEffect(() => {
    if (user) {
      fetchBetHistory(); // Fetch bet history if the user is logged in
    }
  }, [user, fetchBetHistory]); // The effect runs when 'user' or 'fetchBetHistory' changes

  // Display loading spinner or message while authentication or bet history is loading
  if (authLoading || betsLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-accent w-full">
      <Header /> {/* The Header component */}
      <TopNav /> {/* Top Navigation component */}
      <div className="w-full overflow-hidden"> {/* Ensure AutoScrollCarousel doesn't overflow */}
        <AutoScrollCarousel />
      </div>
      <main className="px-4 sm:px-6 lg:px-8 w-full overflow-hidden">
        <LiveMatches /> {/* Display live matches */}
        <QuickSelection /> {/* Quick bet selection options */}
        <SportLists /> {/* List of available sports */}
        {user && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            <BetHistory betHistory={betHistory} /> {/* Display bet history if the user is logged in */}
          </section>
        )}
      </main>
      <Footer /> {/* Footer component */}
      <BackToTop /> {/* Button to scroll back to the top of the page */}
      <Navbar /> {/* Bottom navigation bar */}
    </div>
  );
};

export default HomePage;
