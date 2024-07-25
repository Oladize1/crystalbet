import React from 'react';
import Header from './components/Header';
import Banner from './components/Banner';
import LiveMatches from './components/LiveMatches';
import SportsList from './components/SportsList';
import Footer from './components/Footer';
import './index.css';

const App = () => (
  <div className="App">
    <Header />
    <Banner />
    <LiveMatches />
    <SportsList />
    <Footer />
  </div>
);

export default App;
