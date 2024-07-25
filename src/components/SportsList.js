import React from 'react';

const sports = [
  "Soccer", "Basketball", "Baseball", "Ice Hockey", "Tennis",
  "Handball", "Boxing", "Rugby", "Snooker", "Cricket",
  "Volleyball", "Waterpolo", "MMA"
];

const SportsList = () => (
  <section className="py-10 bg-gray-800 text-white">
    <div className="container mx-auto">
      <h2 className="text-2xl font-bold mb-6">Browse Sports</h2>
      <ul className="space-y-4">
        {sports.map((sport, index) => (
          <li key={index} className="bg-gray-700 p-4 rounded">
            {sport}
          </li>
        ))}
      </ul>
    </div>
  </section>
);

export default SportsList;
