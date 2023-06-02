import React, { useEffect, useState } from 'react';
import { Typography, Box, IconButton, CircularProgress, Paper, Grid, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { fetchEnrolledCourses, fetchAllCourses, handleUnsubscribeFromCourse } from './API_requests.js';
import { Header, LogoImage, LogoutButton } from './common.js';
import { SvgIcon } from '@mui/material';

const UserCoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const userRole = localStorage.getItem('role');
  const [selectedPaper, setSelectedPaper] = useState(null); 

  const unsubscribeFromCourse = async (courseId) => {
    try {
      const response = await handleUnsubscribeFromCourse(courseId);
      console.log('Unsubscribe response:', response);

      if (response.status === 200) {
        setTimeout(() => {
          window.location.href = '/courses';
        }, 500);
      }
    } catch (error) {
      console.error('Error unsubscribing from course:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (userRole === 'student') {
          const enrolledCourses = await fetchEnrolledCourses();
          setCourses(enrolledCourses);
        } else if (userRole === 'teacher') {
          const allCourses = await fetchAllCourses();
          setCourses(allCourses);
        }
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        console.error(error);
      }
    };

    fetchData();
  }, [userRole]);

  const handlePaperClick = (courseId) => {
    setSelectedPaper(courseId);
  };

  const StarIcon = (props) => (
    <SvgIcon {...props}>
      <path
        d="M12 0L15.09 7.14218L22 8.46534L17 14.0779L17.9 21.0578L12 17.8765L6.1 21.0578L7 14.0779L2 8.46534L8.91 7.14218L12 0Z"
        fill="currentColor"
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
          <LogoutButton>Logout</LogoutButton>
        </div>
      </Header>
      <Box sx={{ flexGrow: 1, marginTop: '4rem', textAlign: 'left' }}>
        <IconButton component={Link} to="/dashboard" sx={{ marginRight: 'auto' }}>
            <ArrowBack />
        </IconButton>
        <Typography variant="h4" component="h1" align="center" gutterBottom>
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
                <Paper
                  elevation={3}
                  sx={{
                    padding: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    transition: 'transform 0.3s ease',
                    transform: selectedPaper === course.id ? 'scale(1.05)' : 'scale(1)',
                    cursor: 'pointer',
                    '&:hover': {
                      transform: 'scale(1.05)',
                    },
                  }}
                  onClick={() => handlePaperClick(course.id)}
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
                        Rating: {course.course_rating}
                      </Typography>
                    </div>
                  </div>
                  <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    {userRole === 'student' ? (
                      <Button variant="contained" color="secondary" onClick={() => unsubscribeFromCourse(course.id)}>
                        Unsubscribe
                      </Button>
                    ) : (
                      <Button variant="contained" color="primary" component={Link} to={`/edit-course/${course.id}`}>
                        Edit
                      </Button>
                    )}
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


