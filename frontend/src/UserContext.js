import React, { createContext, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [role, setRole] = useState(null);

  return (
    <UserContext.Provider value={{ userId, setUserId, role, setRole }}>
      {children}
    </UserContext.Provider>
  );
};
