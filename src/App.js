// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import BetsPage from './pages/BetsPage';
import LiveBetsPage from './pages/LiveBetsPage';
import UserProfilePage from './pages/UserProfilePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';
import AZMenu from './components/AZMenu';
import { AuthProvider } from './context/AuthContext';
import { BetProvider } from './context/BetContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <BetProvider>
          <Routes>
            <Route path="/" element={<Layout><HomePage /></Layout>} />
            <Route path="/bets" element={<ProtectedRoute><Layout><BetsPage /></Layout></ProtectedRoute>} />
            <Route path="/live-bets" element={<ProtectedRoute><Layout><LiveBetsPage /></Layout></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Layout><UserProfilePage /></Layout></ProtectedRoute>} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<SignupPage />} />
            <Route path="/AZMenu" element={<Layout><AZMenu /></Layout>} /> {/* Add this line */}
          </Routes>
        </BetProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
