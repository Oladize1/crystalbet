import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { loginUser } from '../services/api'; // Import the login function from api.js

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // Loading state
  const { login } = useContext(AuthContext); // Context for managing user state
  const navigate = useNavigate();

  // Handle the form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous error
    setLoading(true); // Start loading

    try {
      // Prepare the form data in 'application/x-www-form-urlencoded' format
      const formData = new URLSearchParams();
      formData.append('username', email); // The username field in OAuth2PasswordRequestForm maps to email
      formData.append('password', password);

      // Call the login API method
      const response = await loginUser(formData); // Use the imported function

      // On success, call the context login method to store token
      const { access_token } = response.data; // Adjust if your API returns different structure
      login(access_token); // Store the access token in context

      // Redirect the user after successful login
      navigate('/');
    } catch (err) {
      console.error(err);
      setError('Failed to login. Please check your credentials and try again.');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-accent">
      <Header />
      <main className="flex-1 container mx-auto my-16 p-4 flex items-center justify-center">
        <div className="w-full max-w-md bg-white p-8 rounded shadow">
          <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
          {error && <p role="alert" className="text-red-500 mb-4">{error}</p>} {/* Added role for accessibility */}
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
              <label htmlFor="password" className="block text-gray-700">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                required
              />
            </div>
            <button
              type="submit"
              className={`w-full bg-red-600 text-white p-2 rounded hover:bg-red-700 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={loading} // Disable button while loading
            >
              {loading ? 'Logging In...' : 'Login'}
            </button>
          </form>
          <div className="mt-4 text-center">
            <a href="/reset-password" className="text-blue-600 hover:underline">Forgot Password?</a> {/* Password recovery link */}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default LoginPage;
