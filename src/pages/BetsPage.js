import React, { useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { BetContext } from '../context/BetContext';
import Header from '../components/Header';
import BetList from '../components/BetList';
import BetHistory from '../components/BetHistory';
import Footer from '../components/Footer';

const BetsPage = () => {
  const { user, loading: authLoading } = useContext(AuthContext);
  const { bets, loading: betsLoading, fetchBets, fetchBetHistory, betHistory } = useContext(BetContext);

  useEffect(() => {
    fetchBets();
    if (user) {
      fetchBetHistory();
    }
  }, [user, fetchBets, fetchBetHistory]);

  if (authLoading || betsLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex-1 container mx-auto p-4">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Available Bets</h2>
          <BetList bets={bets} />
        </section>
        {user && (
          <section>
            <h2 className="text-2xl font-bold mb-4">Bet History</h2>
            <BetHistory betHistory={betHistory} />
          </section>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default BetsPage;
