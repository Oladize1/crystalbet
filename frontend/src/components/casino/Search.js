import { useState } from 'react';
import { FaSearch } from 'react-icons/fa';

const SearchModal = ({ onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(false);

  const handleSearch = () => {
    // Mock search logic
    if (searchTerm === 'df!ndfl;vzvn') {
      setError(true);
    } else {
      setError(false);
      onClose();
      // Proceed with search action
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-gray-800 p-5 rounded-md w-1/3">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-white">Search</h3>
          <button onClick={onClose} className="text-white">
            &times;
          </button>
        </div>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full p-2 rounded-md mb-4 text-gray-900"
          placeholder="Search..."
        />
        <button
          onClick={handleSearch}
          className="bg-primary-dark w-full p-2 rounded-md text-white"
        >
          <FaSearch />
        </button>
        {error && (
          <p className="mt-4 text-red-500">Error: No results found!</p>
        )}
      </div>
    </div>
  );
};

export default SearchModal;
