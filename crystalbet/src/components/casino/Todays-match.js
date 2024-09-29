import React, { useState } from 'react';

const TodaysEvents = () => {
  const [selectedDay, setSelectedDay] = useState('Today');
  const [selectedSport, setSelectedSport] = useState('Soccer');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedType, setSelectedType] = useState('Popular');

  const daysOptions = ['Today', 'Tomorrow', 'This Week', 'This Month'];
  const sportsOptions = ['Soccer', 'Tennis', 'Basketball', 'Baseball'];
  const categoryOptions = ['All', 'Top Leagues', 'Cups', 'Other'];
  const typeOptions = ['Popular', 'New', 'Ongoing', 'Results'];

  return (
    <div className="bg-accent mt-8 text-white min-h-screen py-8">
      {/* Back Button */}
      <div className="p-4 bg-primary-dark">
        <button className="text-secondary transition-all duration-300 ease-in-out transform hover:scale-105">
          &lt; Today's Events
        </button>
      </div>

      {/* Dropdown Filters */}
      <div className="p-4">
        <div className="grid grid-cols-3 gap-4 mb-4">
          {/* Day Dropdown */}
          <select
            value={selectedDay}
            onChange={(e) => setSelectedDay(e.target.value)}
            className="px-4 py-2 rounded-lg bg-accent-dark text-white w-full transition duration-500 ease-in-out transform hover:bg-primary-dark hover:scale-105"
          >
            {daysOptions.map((day) => (
              <option key={day} value={day}>
                {day.toUpperCase()}
              </option>
            ))}
          </select>

          {/* Sport Dropdown */}
          <select
            value={selectedSport}
            onChange={(e) => setSelectedSport(e.target.value)}
            className="px-4 py-2 rounded-lg bg-accent-dark text-white w-full transition duration-500 ease-in-out transform hover:bg-primary-dark hover:scale-105"
          >
            {sportsOptions.map((sport) => (
              <option key={sport} value={sport}>
                {sport.toUpperCase()}
              </option>
            ))}
          </select>

          {/* Category Dropdown */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 rounded-lg bg-accent-dark text-white w-full transition duration-500 ease-in-out transform hover:bg-primary-dark hover:scale-105"
          >
            {categoryOptions.map((category) => (
              <option key={category} value={category}>
                {category.toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        {/* Type Dropdown */}
        <div className="grid grid-cols-1 gap-4">
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-4 py-2 rounded-lg bg-accent-dark text-white w-full transition duration-500 ease-in-out transform hover:bg-primary-dark hover:scale-105"
          >
            {typeOptions.map((type) => (
              <option key={type} value={type}>
                {type.toUpperCase()}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default TodaysEvents;
