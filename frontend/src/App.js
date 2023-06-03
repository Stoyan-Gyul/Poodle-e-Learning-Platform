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
import PendingStudentsPage from './PendingStudentsPage';
import EditCoursePage from './EditCoursePage';
import CourseReportPage from './CourseReportPage';
import { AuthProvider } from './AuthContext';
import { UserProvider } from './UserContext';


const theme = createTheme();

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <UserProvider>
          <AuthProvider>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/courses" element={<UserCoursesPage />} />
              <Route path="/create-course" element={<CreateCoursePage />} />
              <Route path="/edit-course/:courseId" element={<EditCoursePage />} />
              <Route path="/courses/:courseId/report" element={<CourseReportPage />} />
              <Route path="/pending-approvals" element={<PendingStudentsPage />} />
            </Routes>
          </AuthProvider>
        </UserProvider>
      </Router>
    </ThemeProvider>
  );
};

export default App;
