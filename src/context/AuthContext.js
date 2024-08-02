import React, { createContext, useState, useEffect } from 'react';
import { loginService, signupService, getUserService, logoutService } from '../services/authService';
import { useNavigate } from 'react-router-dom'; // Updated import

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); // Updated usage

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getUserService();
        setUser(userData);
      } catch (error) {
        console.error("Failed to fetch user", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  const login = async (email, password) => {
    const user = await loginService(email, password);
    setUser(user);
    navigate('/'); // Updated usage
  };

  const signup = async (email, username, password) => {
    const user = await signupService(email, username, password);
    setUser(user);
    navigate('/'); // Updated usage
  };

  const logout = () => {
    logoutService();
    setUser(null);
    navigate('/login'); // Updated usage
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
