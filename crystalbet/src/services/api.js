import axios from 'axios';

// Base API URL for FastAPI backend
const API_URL = 'http://localhost:8000/api';

// Create an Axios instance with the base API URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the token to the headers if the user is authenticated
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken'); // Fetch auth token from local storage
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`; // Add token to the request headers
  }
  return config;
});

// Interceptor to handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific status codes, like unauthorized access
      if (error.response.status === 401) {
        localStorage.removeItem('authToken'); // Clear token on unauthorized
        window.location.href = '/login'; // Redirect to login page
      } else if (error.response.status === 403) {
        // Handle forbidden access (optional)
        alert('Access denied.');
      }
    }
    return Promise.reject(error);
  }
);

// ========================== AUTH API ==========================
export const loginUser = (credentials) => api.post('/auth/login', credentials);
export const signupUser = (data) => api.post('/auth/register', data);
export const fetchUserDetails = () => api.get('/users/profile');

// ========================== BETS API ==========================
export const fetchAllBets = () => api.get('/bets'); // Changed from '/bets/bets' to '/bets'
export const fetchLiveBets = () => api.get('/bets/live'); // Ensure this matches your FastAPI endpoint
export const placeBet = (betData) => api.post('/bets/book', betData); // Match the POST route for booking bets
export const fetchBetHistory = () => api.get('/betslip'); // Ensure this matches your FastAPI endpoint

// ========================== CASINO API ==========================
export const fetchCasinoData = () => api.get('/casino'); // Changed from '/bets/casino' to '/casino'
export const fetchCasinoLiveData = () => api.get('/casino/live'); // Ensure this matches your FastAPI endpoint

// ========================== VIRTUAL GAMES API ==========================
export const fetchVirtualGames = () => api.get('/virtuals'); // Ensure this matches your FastAPI endpoint

// ========================== COUPON API ==========================
export const checkCoupon = (couponCode) => api.post('/coupons/check', { couponCode }); // Match the POST route for coupon checking

// ========================== EVENTS API ==========================
export const fetchTodayMatches = () => api.get('/matches/today'); // Ensure this matches your FastAPI endpoint

// ========================== TESTING SERVICES ==========================
const JSONPLACEHOLDER_API_URL = 'https://jsonplaceholder.typicode.com';

// Login service for testing (using JSONPlaceholder)
export const loginService = async (email, password) => {
  try {
    const response = await api.get(`${JSONPLACEHOLDER_API_URL}/users`);
    return response.data[0]; // Returning the first user for testing
  } catch (error) {
    console.error('Login Service Error:', error);
    throw error;
  }
};

// Signup service for testing (using JSONPlaceholder)
export const signupService = async (email, username, password) => {
  try {
    const response = await api.post(`${JSONPLACEHOLDER_API_URL}/users`, {
      email,
      username,
      password,
    });
    return response.data; // Returning the created user
  } catch (error) {
    console.error('Signup Service Error:', error);
    throw error;
  }
};

// Logout service (localStorage removal)
export const logoutService = async () => {
  try {
    localStorage.removeItem('authToken'); // Ensure the key is correct
    return true;
  } catch (error) {
    console.error('Logout Service Error:', error);
    throw error;
  }
};

// Export the Axios instance
export default api;
