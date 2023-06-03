import React, { createContext, useState, useContext } from 'react';
import { UserContext } from './UserContext';

// Create the AuthContext
export const AuthContext = createContext();

// Create the AuthProvider component
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState('');
  const { setUserId, setRole} = useContext(UserContext)

  // Function to set the token
  const setAuthToken = (newToken) => {
    setToken(newToken);
  };

  const logout = () => {
    // Remove the token from local storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');

    // Clear the token, user_id, and role from the app state
    setAuthToken('');
    setUserId('');
    setRole('');
  };

  console.log(token);
  return (
    <AuthContext.Provider value={{ token, setAuthToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
