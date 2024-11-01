// src/pages/SignupPage.js
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { signupUser } from '../services/api'; // Import the signup function from api.js
import Header from '../components/Header';
import Footer from '../components/Footer';
import { AuthContext } from '../context/AuthContext'; // Assuming you have an AuthContext

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await signupUser({ email, username, password });

      if (response.user_id) { // Check if registration was successful
        // Here, set user information if required
        setUser({ email, username });
        navigate('/');
      }
    } catch (err) {
      setError('Failed to sign up. Please check your details and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-accent">
      <Header />
      <main className="flex-1 container my-16 mx-auto p-4 flex items-center justify-center">
        <div className="w-full max-w-md bg-secondary p-8 rounded shadow">
          <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>
          {error && <p className="text-red-500 mb-4">{error}</p>}
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="username" className="block text-gray-700">Username</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password" className="block text-gray-700">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                required
                minLength={6}
              />
            </div>
            <button
              type="submit"
              className={`w-full bg-red-600 text-white p-2 rounded hover:bg-red-700 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={loading}
            >
              {loading ? 'Signing Up...' : 'Sign Up'}
            </button>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default SignupPage;
