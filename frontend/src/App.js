import * as React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import HomePage from './HomePage';
import LoginPage from './LoginPage';
import SignupPage from './SignupPage';
import DashboardPage from './DashboardPage';
import ProfilePage from './ProfilePage';
import UserCoursesPage from './UserCoursesPage';
import CreateCoursePage from './CreateNewCourse';
import { AuthProvider } from './AuthContext';
import { UserProvider } from './UserContext';

const theme = createTheme();

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AuthProvider>
        <UserProvider>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/profile" element={<ProfilePage/>} />
            <Route path="/courses" element={<UserCoursesPage/>} />
            <Route path="/create-course" element={<CreateCoursePage/>} />
          </Routes>
          </UserProvider>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
};

export default App;
