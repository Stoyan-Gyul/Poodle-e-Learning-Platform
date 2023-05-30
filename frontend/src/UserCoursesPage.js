import React, { useEffect, useState } from 'react';
import { Typography, Box, IconButton, CircularProgress, Paper, Grid, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { fetchEnrolledCourses, handleUnsubscribeFromCourse } from './API_requests.js';
import { Header, LogoImage } from './common.js';
import { common } from '@mui/material/colors';

const UserCoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const unsubscribeFromCourse = async (courseId) => {
    try {
      const response = await handleUnsubscribeFromCourse(courseId);
      console.log('Unsubscribe response:', response);

      if (response.status === 200) {
        setTimeout(() => {
          window.location.href = '/user-courses';
        }, 500);
      }
    } catch (error) {
      console.error('Error unsubscribing from course:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const enrolledCourses = await fetchEnrolledCourses();

        setCourses(enrolledCourses);
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box sx={{ flexGrow: 1, marginTop: '4rem', textAlign: 'left' }}>
        <Box display="flex" alignItems="center" justifyContent="center" mb={2}>
          <IconButton component={Link} to="/dashboard" sx={{ marginRight: 'auto' }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" component="h1" align="center" gutterBottom>
            My Courses
          </Typography>
          <Box sx={{ width: '630px' }} /> {/* Add an empty box for spacing */}
        </Box>
        {isLoading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="200px">
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={2}>
            {courses.map((course) => (
              <Grid item key={course.id} xs={12} sm={6} md={4}>
                <Paper elevation={3} sx={{ padding: '1rem', display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <div style={{ flex: '1', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>
                      {course.title}
                    </Typography>
                    <Typography variant="body2" gutterBottom>
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
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100px' }}>
                    {course.home_page_pic ? (
                      <img src={`data:image/jpeg;base64,${course.home_page_pic}`} alt="Course Pic" style={{ width: '100px', height: '100px' }} />
                    ) : (
                      <div
                        style={{
                          width: '100px',
                          height: '100px',
                          border: '1px solid black',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <Typography variant="body2" color="textSecondary">
                          No Image
                        </Typography>
                      </div>
                    )}
                  </div>
                  <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <Button variant="contained" color="secondary" onClick={() => unsubscribeFromCourse(course.id)}>
                      Unsubscribe
                    </Button>
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

