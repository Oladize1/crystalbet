// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import BetsPage from './pages/BetsPage';
import LiveBetsPage from './pages/LiveBetsPage';
import UserProfilePage from './pages/UserProfilePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';

// Buttom nav links
import AZMenu from './components/sub_menu/AZMenu';
import QuickLinks from './components/sub_menu/QuickLinks';
import BookABet from './components/bottom_nav_items/BookABet'
import BetSlip from './components/bottom_nav_items/BetSlip'
import Live from './components/bottom_nav_items/Live'

//Home page content
import SportsPage from './components/SportList_content.js/SportsPage';
import LiveMatchStream from './components/liveStream_content/LiveMatchStream';
import MatchDetails from './components/liveStream_content/MatchDetails'

//TopNav pages
import Casino from './components/casino/Casino'
import CasinoLive from './components/casino/CasinoLive'
import Virtual from './components/casino/Virtual'
import CouponCheck from './components/casino/CouponCheck';
import HelpPage from './components/casino/Help';
import OddsLessThan from './components/casino/OddsLessThan'
import TodaysMatch from './components/casino/Todays-match'

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
            <Route path="/AZMenu" element={<Layout><AZMenu /></Layout>}/> 
            <Route path="/quick-links" element={<Layout><QuickLinks /></Layout>}/>
            <Route path="book-bet" element={<Layout><BookABet/></Layout>}/>
            <Route path="betslip" element={<Layout><BetSlip/></Layout>}/>
            <Route path="live" element={<Layout><Live/></Layout>}/>
            <Route path="/sports/:category" element={<Layout><SportsPage /></Layout>} />
            <Route path="/live-stream/:matchId" element={<Layout><LiveMatchStream /></Layout>} />
            <Route path="/match/:id" element={<Layout><MatchDetails /></Layout>} />
            <Route path="/casino" element={<Layout><Casino /></Layout>} />
            <Route path="/casino-live" element={<Layout><CasinoLive /></Layout>} />
            <Route path="/virtuals" element={<Layout><Virtual /></Layout>} />
            <Route path="/coupon-check" element={<Layout><CouponCheck /></Layout>} /> 
           <Route path="/cms" element={<Layout><HelpPage /></Layout>} />
           <Route path="/odds-less-than" element={<Layout><OddsLessThan /></Layout>} />
           <Route path="/todays-event" element={<Layout><TodaysMatch /></Layout>} />
          </Routes>
        </BetProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
