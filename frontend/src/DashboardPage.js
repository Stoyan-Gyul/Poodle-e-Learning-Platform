import React, { useEffect, useState } from 'react';
import { Grid, Box, Typography, Paper, IconButton, InputBase, Avatar, Menu, MenuItem } from '@mui/material';
import { styled } from '@mui/system';
import { HomeOutlined, PersonOutlined, BookOutlined, SearchOutlined, AddCircleOutline } from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';

import logoImage from './images/logo.png';
import { fetchAllCourses } from './API_requests'; // Import the fetchAllCourses function

const LogoIcon = styled(Avatar)(({ theme }) => ({
  width: theme.spacing(8),
  height: theme.spacing(8),
  marginBottom: theme.spacing(2),
}));

const SearchContainer = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.common.white,
  '&:hover': {
    backgroundColor: theme.palette.common.white,
  },
  marginLeft: 0,
  width: '100%',
  border: `1px solid ${theme.palette.divider}`,
}));

const SearchIconContainer = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const SearchInput = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  padding: theme.spacing(1, 1, 1, 0),
  paddingLeft: `calc(1em + ${theme.spacing(4)})`,
  transition: theme.transitions.create('width'),
}));

const VerticalLine = styled('div')(({ theme }) => ({
  borderRight: `1px solid ${theme.palette.divider}`,
  height: '100%',
  position: 'absolute',
  top: 0,
  left: '20',
  transform: 'translateX(-50%)',
}));

const CourseList = ({ courses }) => {
  return (
    <Box mt={4} px={4}>
      <Grid container spacing={2}>
        {courses.map((course) => (
          <Grid item key={course.id} xs={12} sm={6}>
            <Paper elevation={3} sx={{ p: 2, mb: 2, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
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
                {/* Add the rest of the course data */}
              </div>
              <div style={{ flex: 1 }}></div>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [courses, setCourses] = useState([]);
  const userRole = localStorage.getItem('role');

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    navigate('/profile');
    handleMenuClose();
  };

  const handleCoursesClick = () => {
    navigate('/courses');
    handleMenuClose();
  };

  const handleCreateCourseClick = () => {
    navigate('/create-course');
    handleMenuClose();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedCourses = await fetchAllCourses();
        setCourses(fetchedCourses);
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container>
        {/* Left Section */}
        <Grid item xs={2.5}>
          <Box textAlign="center" mt={4} ml={13}>
            <LogoIcon alt="Logo Icon" src={logoImage} />
          </Box>
          <Box mt={4}>
            <Box mb={2}>
              <MenuItem
                onClick={handleMenuClose}
                component={Link}
                to="/"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: '#1976d2',
                  },
                }}
              >
                <IconButton>
                  <HomeOutlined />
                </IconButton>
                Home
              </MenuItem>
            </Box>
            <Box mb={2}>
              <MenuItem
                onClick={handleProfileClick}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: '#1976d2',
                  },
                }}
              >
                <IconButton>
                  <PersonOutlined />
                </IconButton>
                Profile
              </MenuItem>
            </Box>
            <Box mb={2}>
              <MenuItem
                onClick={handleCoursesClick}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: '#1976d2',
                  },
                }}
              >
                <IconButton>
                  <BookOutlined />
                </IconButton>
                My Courses
              </MenuItem>
            </Box>
            {userRole === 'teacher' && (
              <Box mb={2}>
                <MenuItem
                  component={Link}
                  to="/create-course"
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    paddingLeft: '20px',
                    '&:hover': {
                      backgroundColor: '#1976d2',
                    },
                  }}
                >
                  <IconButton>
                    <AddCircleOutline />
                  </IconButton>
                  Create New Course
                </MenuItem>
              </Box>
            )}
          </Box>
        </Grid>

        {/* Vertical Line */}
        <Grid item xs={1}>
          <VerticalLine />
        </Grid>

        {/* Right Section */}
        <Grid item xs={8}>
          <Box display="flex" justifyContent="flex-end" mt={4} pr={4}>
            <SearchContainer>
              <SearchIconContainer>
                <SearchOutlined />
              </SearchIconContainer>
              <SearchInput placeholder="Search..." />
            </SearchContainer>
            {/* temporary added for visivility */}
            <Typography variant="body1" component="p">
                User ID: {localStorage.getItem('user_id')}
            </Typography>
            <Typography variant="body1" component="p">
                Role: {localStorage.getItem('role')}
            </Typography>
          </Box>
          <CourseList courses={courses} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
