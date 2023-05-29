import React, { useEffect, useState } from 'react';
import { Typography, Box, CircularProgress, Paper, Grid } from '@mui/material';
import { styled } from '@mui/system';
import logoImage from './images/logo.png';

const Header = styled('header')({
  position: 'absolute',
  top: '0',
  left: '0',
  right: '0',
  display: 'flex',
  justifyContent: 'flex-start',
  alignItems: 'center',
  width: '100%',
  backgroundColor: '#e8f0fe', // Replace with your desired background color
  padding: '0.1rem',
  borderTop: '1px solid #7d68a1',
});

const LogoImage = styled('img')({
  width: '50px',
  height: '50px',
  borderRadius: '50%',
});

const UserCoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchEnrolledCourses = async () => {
    const authToken = localStorage.getItem('authToken');

    try {
      const response = await fetch('http://localhost:8000/courses/enrolled_courses', {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      const data = await response.json();

      if (Array.isArray(data)) {
        setCourses(data);
      } else {
        setCourses([]);
      }

      setIsLoading(false);
    } catch (error) {
      console.log('Error fetching enrolled courses:', error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEnrolledCourses();
  }, []);

  return (
  <>
    <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
    </Header>
    <Box sx={{ flexGrow: 1, marginTop: '4rem' }}>
      <Typography variant="h4" align="center" gutterBottom>
        My Courses
      </Typography>
      {isLoading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="200px">
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={2}>
          {courses.map((course) => (
            <Grid item key={course.id} xs={12} sm={6} md={4}>
              <Paper elevation={3} sx={{ padding: '1rem', display: 'flex' }}>
                <div style={{ flex: '1' }}>
                  <Typography variant="h6" gutterBottom>
                    {course.title}
                  </Typography>
                  <Typography variant="body1" gutterBottom>
                    {course.description}
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    Rating: {course.course_rating}
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    Expertise Area: {course.expertise_area}
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    Objective: {course.objective}
                  </Typography>
                </div>
                <div style={{ flex: '1', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <div style={{ width: '100px', height: '100px', border: '1px solid black', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography variant="body2" color="textSecondary">
                      Course Pic
                    </Typography>
                  </div>
                </div>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
    </>
  );
};

export default UserCoursesPage;




