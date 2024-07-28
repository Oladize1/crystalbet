import React from 'react';
import Header from './components/Header';
import Banner from './components/Banner';
import LiveMatches from './components/LiveMatches';
import SportsList from './components/SportsList';
import QuickSelection from './components/QuickSelection'
// import DynamicSlides from './components/DynamicSlider';
import Footer from './components/Footer';
import BottomNav from './components/BottomNav'
import './index.css';

const App = () => (
  <div className="App">
    <div className='min-h-screen flex flex-col'>
      <div className='h-full'>
    <Header />
    {/* <DynamicSlides/> */}
    <Banner />
    <LiveMatches />
    <QuickSelection/>
    <SportsList />
    <Footer />
      </div>
    <BottomNav/>
    </div>
  </div>
);

export default App;
