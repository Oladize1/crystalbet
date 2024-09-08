import React, { useState } from 'react';

const OddsLessThan = () => {
  const [selectedOdd, setSelectedOdd] = useState(1.25); // Default max odd
  const [selectedTimeRange, setSelectedTimeRange] = useState('1 hr'); // Default time range
  const [selectedSport, setSelectedSport] = useState('Calcio'); // Default sport
  const [eventsAvailable, setEventsAvailable] = useState(true); // Placeholder for event check

  const maxOdds = [1.25, 1.5, 1.75, 2]; // Max odds options
  const timeRanges = ['1 hr', '3 hrs', 'Today', '3 Days']; // Time range options
  const sports = [
    { name: 'Calcio', count: 2 },
    { name: 'Baseball', count: 6 },
    { name: 'Hockey', count: 1 },
    { name: 'Rugby', count: 1 }
  ];

  const handleOddClick = (odd) => {
    setSelectedOdd(odd);
    // Add any logic to filter based on selected odd
  };

  const handleTimeRangeClick = (range) => {
    setSelectedTimeRange(range);
    // Add any logic to filter based on time range
  };

  const handleSportClick = (sport) => {
    setSelectedSport(sport.name);
    // Add any logic to filter events by sport
  };

  return (
    <div className="text-white min-h-screen my-8 py-8">
      {/* Back Button */}
      <div className="p-4 bg-primary-dark">
        <button className="text-secondary">&lt; Odds Filter</button>
      </div>

      {/* Max Odd Filter */}
      <div className="p-4 w-full">
        <h2 className="mb-2 text-lg">Choose the max odd to show</h2>
        <div className="grid grid-cols-4 gap-4">
          {maxOdds.map((odd) => (
            <button
              key={odd}
              onClick={() => handleOddClick(odd)}
              className={`px-4 py-2 rounded-lg text-center ${selectedOdd === odd ? 'bg-primary-dark' : 'bg-accent-dark'}`}
            >
              {odd}
            </button>
          ))}
        </div>
      </div>

      {/* Time Range Filter */}
      <div className="p-4 w-full">
        <h2 className="mb-2 text-lg">Choose the time range you wish to show</h2>
        <div className="grid grid-cols-4 gap-4">
          {timeRanges.map((range) => (
            <button
              key={range}
              onClick={() => handleTimeRangeClick(range)}
              className={`px-4 py-2 rounded-md text-center ${selectedTimeRange === range ? 'bg-primary-dark' : 'bg-accent-dark'}`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Sports Filter */}
      <div className="p-4 w-full">
        <div className="grid grid-cols-4 gap-4">
          {sports.map((sport) => (
            <button
              key={sport.name}
              onClick={() => handleSportClick(sport)}
              className={`px-4 py-2 rounded-md flex justify-between ${
                selectedSport === sport.name ? 'bg-primary-dark' : 'bg-accent-dark'
              }`}
            >
              <span>{sport.name}</span>
              <span>{sport.count}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Events Section */}
      <div className="p-4 bg-white w-full text-center text-accent">
        {eventsAvailable ? (
          <div className="text-lg">Event list based on selected filters...</div>
        ) : (
          <div className="text-accent">No event available</div>
        )}
      </div>
    </div>
  );
};

export default OddsLessThan;
