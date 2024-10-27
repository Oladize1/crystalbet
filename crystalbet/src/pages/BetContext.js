import React, { createContext, useState } from 'react';
import api from '../api';

export const BetContext = createContext();

export const BetProvider = ({ children }) => {
  const [liveBets, setLiveBets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLiveBets = async () => {
    try {
      const response = await api.get('/bets/live');
      setLiveBets(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching live bets:', error);
      setLoading(false);
    }
  };

  return (
    <BetContext.Provider value={{ liveBets, loading, fetchLiveBets }}>
      {children}
    </BetContext.Provider>
  );
};
