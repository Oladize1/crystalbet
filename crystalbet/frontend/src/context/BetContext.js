import React, { createContext, useState, useEffect } from 'react';
import { fetchAllBets, fetchLiveBets, placeBet, fetchBetHistory } from '../services/api'; // Assuming fetchBetHistory is defined in api.js

export const BetContext = createContext();

export const BetProvider = ({ children }) => {
  const [bets, setBets] = useState([]);
  const [liveBets, setLiveBets] = useState([]);
  const [betHistory, setBetHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all bets
  const loadBets = async () => {
    try {
      const { data } = await fetchAllBets();
      setBets(data);
    } catch (err) {
      setError('Failed to fetch bets.');
      console.error('Failed to fetch bets:', err);
    }
  };

  // Fetch live bets
  const loadLiveBets = async () => {
    try {
      const { data } = await fetchLiveBets();
      setLiveBets(data);
    } catch (err) {
      setError('Failed to fetch live bets.');
      console.error('Failed to fetch live bets:', err);
    }
  };

  // Fetch bet history
  const loadBetHistory = async () => {
    try {
      setLoading(true); // Set loading to true while fetching
      const { data } = await fetchBetHistory(); // Assuming this is an API call to fetch the bet history
      setBetHistory(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch bet history.');
      setLoading(false);
      console.error('Failed to fetch bet history:', err);
    }
  };

  // Place a bet
  const submitBet = async (betData) => {
    try {
      const { data } = await placeBet(betData);
      // Handle success logic, such as updating bet history
      setBetHistory((prevHistory) => [...prevHistory, data]); // Add the new bet to the history
      console.log('Bet placed successfully:', data);
    } catch (err) {
      setError('Failed to place bet.');
      console.error('Failed to place bet:', err);
    }
  };

  // Initial data fetching
  useEffect(() => {
    loadBets();
    loadLiveBets();
    loadBetHistory();
  }, []);

  return (
    <BetContext.Provider value={{
      bets,
      liveBets,
      betHistory,
      loading,
      error,
      submitBet,
      loadBetHistory, // If you need to refetch bet history
    }}>
      {children}
    </BetContext.Provider>
  );
};
