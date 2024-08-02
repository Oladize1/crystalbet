import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import BetsPage from './pages/BetsPage';
import LiveBetsPage from './pages/LiveBetsPage';
import UserProfilePage from './pages/UserProfilePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';
import { AuthProvider } from './context/AuthContext';
import { BetProvider } from './context/BetContext';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <BetProvider>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/bets" element={<ProtectedRoute><BetsPage /></ProtectedRoute>} />
            <Route path="/live-bets" element={<ProtectedRoute><LiveBetsPage /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<SignupPage />} />
          </Routes>
        </BetProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
