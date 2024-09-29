// Mock data for demonstration purposes
const mockBets = [
  { id: 1, title: 'Bet 1', description: 'Description for Bet 1' },
  { id: 2, title: 'Bet 2', description: 'Description for Bet 2' },
];

const mockBetHistory = [
  { id: 1, title: 'Bet 1', status: 'Won' },
  { id: 2, title: 'Bet 2', status: 'Lost' },
];

export const fetchBetsService = async () => {
  // Simulate a delay to mimic an API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockBets);
    }, 500);
  });
};

export const placeBetService = async (betDetails) => {
  // Simulate placing a bet and returning the new bet
  return new Promise((resolve) => {
    setTimeout(() => {
      const newBet = { id: Math.random(), ...betDetails };
      mockBets.push(newBet);
      resolve(newBet);
    }, 1000);
  });
};

export const fetchBetHistoryService = async () => {
  // Simulate a delay to mimic an API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockBetHistory);
    }, 1000);
  });
};
