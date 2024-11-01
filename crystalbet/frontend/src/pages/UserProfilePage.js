import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { fetchUserDetails } from '../services/api'; // Import the fetch user details function
import Header from '../components/Header';
import Footer from '../components/Footer';

const UserProfilePage = () => {
  const { user, loading: authLoading } = useContext(AuthContext);
  const [userDetails, setUserDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const getUserDetails = async () => {
      try {
        // Fetch user details if user is authenticated
        const response = await fetchUserDetails(user.token); // Assuming token is part of user
        setUserDetails(response.data); // Set user details
      } catch (err) {
        console.error(err);
        setError('Failed to fetch user details.'); // Handle error
      } finally {
        setLoading(false); // Stop loading regardless of success or failure
      }
    };

    if (user) {
      getUserDetails(); // Fetch user details if user is authenticated
    } else {
      setLoading(false); // Stop loading if user is not authenticated
    }
  }, [user]);

  if (authLoading || loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>; // Show error message if any
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex-1 container mx-auto p-4">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">User Profile</h2>
          <div className="p-4 bg-white shadow rounded">
            <h3 className="text-xl font-bold">{userDetails.name}</h3>
            <p>Email: {userDetails.email}</p>
            <p>Username: {userDetails.username}</p>
            {/* Add more user details as needed */}
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default UserProfilePage;
