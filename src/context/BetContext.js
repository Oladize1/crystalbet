import React, { createContext, useState, useEffect } from 'react';

export const BetContext = createContext();

export const BetProvider = ({ children }) => {
  const [betHistory, setBetHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBetHistory = async () => {
    // Simulate fetching bet history
    setTimeout(() => {
      setBetHistory([{ id: 1, bet: 'Sample Bet' }]); // Simulate bet history data
      setLoading(false);
    }, 2000);
  };

  useEffect(() => {
    fetchBetHistory();
  }, []);

  return (
    <BetContext.Provider value={{ betHistory, loading, fetchBetHistory }}>
      {children}
    </BetContext.Provider>
  );
};
