import React, { useEffect, useState } from 'react';
import { Grid, Box, Button, Typography, Paper, IconButton, InputBase, Avatar, Menu, MenuItem } from '@mui/material';
import { styled } from '@mui/system';
import { HomeOutlined, PersonOutlined, BookOutlined, SearchOutlined, AddCircleOutline } from '@mui/icons-material';
import { SvgIcon } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import logoImage from './images/logo.png';
import { fetchAllCourses, handleSubscribeToCourse } from './API_requests'; // Import the fetchAllCourses 
import PendingActionsIcon from '@mui/icons-material/PendingActions';

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

const subscribeToCourse = async (courseId) => {
  try {
    const response = await handleSubscribeToCourse(courseId);
    console.log('Subscribe response:', response);

    if (response.status === 200) {
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 500);
    }
  } catch (error) {
    console.error('Error subscribing to course:', error);
  }

};

const CourseList = ({ courses }) => {
  const [selectedPaper, setSelectedPaper] = useState(null); 
  const userRole = localStorage.getItem('role');

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
    <Box mt={4} px={4}>
      <Grid container spacing={2}>
        {courses.map((course) => (
          <Grid item key={course.id} xs={12} sm={6}>
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
                      <Button variant="contained" color="primary" onClick={() => subscribeToCourse(course.id)}>
                        Subscribe
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
    </Box>
  );
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [courses, setCourses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredCourses, setFilteredCourses] = useState([]);
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

  const handlePendingApprovalsClick = () => {
    navigate('/pending-approvals');
    handleMenuClose();
  };

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
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

  useEffect(() => {
    const filterCourses = () => {
      const filtered = courses.filter((course) => {
        const { title, expertise_area } = course;
        const searchTerm = searchQuery.toLowerCase();
        return title.toLowerCase().includes(searchTerm) || expertise_area.toLowerCase().includes(searchTerm);
      });
      setFilteredCourses(filtered);
    };

    filterCourses();
  }, [searchQuery, courses]);

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
            {userRole === 'teacher' && (
              <Box mb={2}>
                <MenuItem
                  onClick={handlePendingApprovalsClick}
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
                    <PendingActionsIcon />
                  </IconButton>
                  Pending Approvals
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
              <SearchInput
                placeholder="Search..."
                value={searchQuery}
                onChange={handleSearch}
              />
            </SearchContainer>
            {/* temporary added for visibility */}
            <Typography variant="body1" component="p">
              User ID: {localStorage.getItem('user_id')}
            </Typography>
            <Typography variant="body1" component="p">
              Role: {localStorage.getItem('role')}
            </Typography>
          </Box>
          <CourseList courses={filteredCourses} />
        </Grid>
      </Grid>
    </Box>
  );
  
};

export default Dashboard;
