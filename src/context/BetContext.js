import React, { createContext, useState, useEffect } from 'react';
import { fetchBetsService, placeBetService, fetchBetHistoryService } from '../services/betService';

const BetContext = createContext();

const BetProvider = ({ children }) => {
  const [bets, setBets] = useState([]);
  const [betHistory, setBetHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBets = async () => {
      try {
        const fetchedBets = await fetchBetsService();
        setBets(fetchedBets);
      } catch (error) {
        console.error('Failed to fetch bets', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBets();
  }, []);

  const placeBet = async (betDetails) => {
    try {
      const newBet = await placeBetService(betDetails);
      setBets((prevBets) => [...prevBets, newBet]);
    } catch (error) {
      console.error('Failed to place bet', error);
      throw error;
    }
  };

  const fetchBetHistory = async () => {
    try {
      const fetchedHistory = await fetchBetHistoryService();
      setBetHistory(fetchedHistory);
    } catch (error) {
      console.error('Failed to fetch bet history', error);
    }
  };

  return (
    <BetContext.Provider value={{ bets, betHistory, loading, placeBet, fetchBetHistory }}>
      {children}
    </BetContext.Provider>
  );
};

export { BetProvider, BetContext };
