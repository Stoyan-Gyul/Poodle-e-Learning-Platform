import React, { useEffect, useState, useContext } from 'react';
import { Typography, Box, IconButton, CircularProgress, Paper, Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions, Rating } from '@mui/material';
import { Link } from 'react-router-dom';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { fetchEnrolledCourses, fetchAllCourses, handleUnsubscribeFromCourse, handleRateCourse } from './API_requests.js';
import { Header, LogoImage, LogoutButton } from './common.js';
import { AuthContext } from './AuthContext';
import { SvgIcon } from '@mui/material';


const UserCoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const userRole = localStorage.getItem('role');
  const [selectedPaper, setSelectedPaper] = useState(null);
  const { logout } = useContext(AuthContext);
  const [openDialog, setOpenDialog] = useState(false);
  const [rating, setRating] = useState(0);
  const [selectedCourseId, setSelectedCourseId] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const handleOpenDialog = (courseId) => {
    setSelectedCourseId(courseId);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleRatingChange = (event, newRating) => {
    setRating(newRating);
  };

  const handleRate = async () => {
    try {
      const response = await handleRateCourse(selectedCourseId, rating);
      console.log('Your rating', response);
      setOpenDialog(false);
    } catch (error) {
      console.error(error); // Error message
      setErrorMessage(error.message);
    }
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

  const handlePaperClick = (courseId) => {
    setSelectedPaper(courseId);
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
          <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
        </div>
      </Header>
      <Box sx={{ flexGrow: 1, marginTop: '4rem', textAlign: 'left' }}>

        <Dialog open={openDialog} onClose={handleCloseDialog}>
          <DialogTitle>Rate the Course</DialogTitle>

          {errorMessage && (
            <Typography variant="body2" color="error">
              {errorMessage}
            </Typography>
          )}
          <DialogContent>
            <Rating
              name="rating"
              value={rating}
              onChange={handleRatingChange}
              precision={0.5}
              max={10}
              size="large"
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button onClick={handleRate} disabled={rating === 0} variant="contained" color="primary">
              Rate
            </Button>
          </DialogActions>
        </Dialog>
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
                        Rating: {course.course_rating}/10
                      </Typography>
                    </div>
                    {userRole === 'student' && (
                      <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'space-between' }}>
                        <Button variant="contained" color="primary" onClick={() => unsubscribeFromCourse(course.id)}>
                          Unsubscribe
                        </Button>
                        <Button variant="contained" color="primary" onClick={() => handleOpenDialog(course.id)}>
                          Rate
                        </Button>
                      </div>
                    )}
                    {userRole === 'teacher' && (
                      <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
                          <Button variant="contained" color="primary" component={Link} to={`/edit-course/${course.id}`}>
                            Edit
                          </Button>
                          <Button variant="contained" color="primary" component={Link} to={`/courses/${course.id}/report`}>
                            Run Report
                          </Button>
                        </Box>
                      </div>
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
