import React, { createContext, useState } from 'react';

// Create the AuthContext
export const AuthContext = createContext();

// Create the AuthProvider component
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState('');

  // Function to set the token
  const setAuthToken = (newToken) => {
    setToken(newToken);
  };
  console.log(token);
  return (
    <AuthContext.Provider value={{ token, setAuthToken }}>
      {children}
    </AuthContext.Provider>
  );
};
