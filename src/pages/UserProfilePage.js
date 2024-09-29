import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';

const UserProfilePage = () => {
  const { user, loading: authLoading } = useContext(AuthContext);
  const [userDetails, setUserDetails] = useState(null);

  useEffect(() => {
    if (user) {
      // Fetch user details if needed
      setUserDetails(user); // Assuming user contains the details
    }
  }, [user]);

  if (authLoading || !userDetails) {
    return <div>Loading...</div>;
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
