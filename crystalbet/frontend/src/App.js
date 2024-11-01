import React, { Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { BetProvider } from './context/BetContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

// Lazy-loaded components for performance optimization
const HomePage = React.lazy(() => import('./pages/HomePage'));
const BetsPage = React.lazy(() => import('./pages/BetsPage'));
const LiveBetsPage = React.lazy(() => import('./pages/LiveBetsPage'));
const UserProfilePage = React.lazy(() => import('./pages/UserProfilePage'));
const LoginPage = React.lazy(() => import('./pages/LoginPage'));
const SignupPage = React.lazy(() => import('./pages/SignUpPage'));

// Lazy-loaded bottom nav links
const AZMenu = React.lazy(() => import('./components/sub_menu/AZMenu'));
const QuickLinks = React.lazy(() => import('./components/sub_menu/QuickLinks'));
const BookABet = React.lazy(() => import('./components/bottom_nav_items/BookABet'));
const BetSlip = React.lazy(() => import('./components/bottom_nav_items/BetSlip'));
const Live = React.lazy(() => import('./components/bottom_nav_items/Live'));

// Lazy-loaded top nav content
const Casino = React.lazy(() => import('./components/casino/Casino'));
const CasinoLive = React.lazy(() => import('./components/casino/CasinoLive'));
const Virtual = React.lazy(() => import('./components/casino/Virtual'));
const CouponCheck = React.lazy(() => import('./components/casino/CouponCheck'));
const HelpPage = React.lazy(() => import('./components/casino/Help'));
const OddsLessThan = React.lazy(() => import('./components/casino/OddsLessThan'));
const TodaysMatch = React.lazy(() => import('./components/casino/Todays-match'));

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <BetProvider>
          <Suspense fallback={<div className="text-center p-4">Loading... Please wait.</div>}>
            <Routes>
              <Route path="/" element={<Layout><HomePage /></Layout>} />
              <Route path="/bets" element={<ProtectedRoute><Layout><BetsPage /></Layout></ProtectedRoute>} />
              <Route path="/live-bets" element={<ProtectedRoute><Layout><LiveBetsPage /></Layout></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><Layout><UserProfilePage /></Layout></ProtectedRoute>} />
              <Route path="/login" element={<Layout><LoginPage /></Layout>} />
              <Route path="/register" element={<Layout><SignupPage /></Layout>} />

              {/* Bottom navigation routes */}
              <Route path="/AZMenu" element={<Layout><AZMenu /></Layout>} />
              <Route path="/quick-links" element={<Layout><QuickLinks /></Layout>} />
              <Route path="/book-bet" element={<Layout><BookABet /></Layout>} />
              <Route path="/betslip" element={<Layout><BetSlip /></Layout>} />
              <Route path="/live" element={<Layout><Live /></Layout>} />

              {/* Casino routes */}
              <Route path="/casino" element={<Layout><Casino /></Layout>} />
              <Route path="/casino-live" element={<Layout><CasinoLive /></Layout>} />
              <Route path="/virtuals" element={<Layout><Virtual /></Layout>} />
              <Route path="/coupon-check" element={<Layout><CouponCheck /></Layout>} />
              <Route path="/cms" element={<Layout><HelpPage /></Layout>} />
              <Route path="/odds-less-than" element={<Layout><OddsLessThan /></Layout>} />
              <Route path="/todays-event" element={<Layout><TodaysMatch /></Layout>} />
            </Routes>
          </Suspense>
        </BetProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
