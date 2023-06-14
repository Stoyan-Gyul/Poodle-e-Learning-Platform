import React, { useEffect, useState, useContext } from 'react';
import { Typography, Box, IconButton, CircularProgress, Paper, Grid, Button, SvgIcon } from '@mui/material';
import { Link } from 'react-router-dom';
import { ArrowBack, Star } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { fetchPendingCourses, handleUnsubscribeFromCourse } from './API_requests.js';
import { Header, LogoImage, LogoutButton } from './common.js';
import { AuthContext } from './AuthContext';

const PendingCoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const { logout } = useContext(AuthContext);

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const unsubscribeFromCourse = async (courseId) => {
    try {
      const response = await handleUnsubscribeFromCourse(courseId);
      console.log('Unsubscribe response:', response);
      window.location.reload();
    } catch (error) {
      console.error('Error unsubscribing from course:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const pendingCourses = await fetchPendingCourses();
        setCourses(pendingCourses);
        setIsLoading(false);
      } catch (error) {
        console.error(error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const StarIcon = (props) => (
    <SvgIcon {...props}>
      <path
        d="M12 0L15.09 7.14218L22 8.46534L17 14.0779L17.9 21.0578L12 17.8765L6.1 21.0578L7 14.0779L2 8.46534L8.91 7.14218L12 0Z" 
        stroke="black"  
        strokeWidth="1"
      />
    </SvgIcon>
  );
  
  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
        <div style={{ marginLeft: 'auto' }}>
          <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
        </div>
      </Header>
      <Box sx={{ flexGrow: 1, marginTop: '4rem', textAlign: 'left' }}>
        <IconButton component={Link} to="/dashboard" sx={{ marginRight: 'auto' }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" component="h1" align="center" gutterBottom>
          Pending Courses
        </Typography>
        {isLoading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="200px">
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={2}>
            {courses.map((course) => (
              <Grid item key={course.id} xs={12} sm={6} md={4}>
                <Paper
                  elevation={3}
                  sx={{
                    padding: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                  }}
                >
                  <div style={{ height: '50%', position: 'relative' }}>
                    {course.home_page_pic ? (
                      <img
                        src={`data:image/jpeg;base64,${course.home_page_pic}`}
                        alt="Course Pic"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    ) : (
                      <div
                        style={{
                          width: '100%',
                          height: '100%',
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
                  <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>
                      {course.title}
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      {course.description}
                    </Typography>
                    <div style={{ display: 'flex', alignItems: 'center', marginTop: 'auto' }}>
                      <StarIcon sx={{ color: 'yellow', marginRight: '0.5rem' }} />
                      <Typography variant="body2" gutterBottom>
                        Rating: {course.course_rating}/10
                      </Typography>
                    </div>
                    <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                      <Button variant="contained" color="primary" onClick={() => unsubscribeFromCourse(course.id)}>
                        Unsubscribe
                      </Button>
                      <Button component={Link} to={`/${course.id}/sections`} variant="contained" color="primary">
                        View
                      </Button>
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

export default PendingCoursesPage;


