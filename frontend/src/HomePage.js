import React, { useState, useEffect } from 'react';
import { Box, Button, Paper, SvgIcon, TextField } from '@mui/material/';
import { Link } from 'react-router-dom';
import { styled } from '@mui/system';
import { Header, LogoImage } from './common.js';
import { fetchAllCourses } from './API_requests.js';
import logoImage from './images/logo.png';
import { SearchOutlined } from '@mui/icons-material';

import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const Title = styled('h1')({
  fontSize: '5rem',
  background: '#1976d2',
  WebkitTextFillColor: 'transparent',
  '-webkit-background-clip': 'text',
  '-moz-background-clip': 'text',
  display: 'inline-block',
  margin: '3rem 0 1rem',
});

const SubTitle = styled('h2')({
  fontSize: '2rem',
  background: '#1976d2',
  WebkitTextFillColor: 'transparent',
  '-webkit-background-clip': 'text',
  '-moz-background-clip': 'text',
  margin: '1rem 0 3rem',
});

const SearchContainer = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.common.white,
  '&:hover': {
    backgroundColor: theme.palette.common.white,
  },
  marginLeft: 0,
  width: '600px', // Adjust the width as needed
  border: `1px solid ${theme.palette.divider}`,
}));

const SearchInput = styled(TextField)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  padding: theme.spacing(1.5, 2, 1.5, 0), // Adjust the padding as needed
  paddingLeft: `calc(1em + ${theme.spacing(3)})`,
  transition: theme.transitions.create('width'),
}));

const SearchIconContainer = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 1.5),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

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

const CourseCard = ({ course }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        width: '300px',
        padding: '1rem',
        marginBottom: '1rem',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        flex: '1 0 auto', // Add this line
      }}
    >
      <h3>{course.title}</h3>
      <p>{course.description}</p>
      <p>Tags: {course.tags.join(', ')}</p>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <StarIcon sx={{ color: 'yellow', marginRight: '0.5rem' }} />
        <p>Rating: {course.course_rating}</p>
      </div>
    </Paper>
  );
};

const HomePage = () => {
  const [courses, setCourses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredCourses, setFilteredCourses] = useState([]);

  const [error, setError] = useState('');
  const [startIndex, setStartIndex] = useState(0);

  const handleSearch = (event) => {
    const searchTerm = event.target.value.toLowerCase();
    setSearchQuery(searchTerm);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedCourses = await fetchAllCourses();
        setCourses(fetchedCourses);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setError('Failed to fetch courses');
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const filterCourses = () => {
      const filtered = courses.filter((course) => {
        const { tags, course_rating } = course;
        const searchTerm = searchQuery.toLowerCase();
  
        // Check if any tag matches the search query
        const tagMatches = tags.some((tag) => tag.toLowerCase().includes(searchTerm));
  
        // Check if course_rating is not null before calling toString
        const ratingMatches = course_rating && course_rating.toString().includes(searchTerm);
  
        return tagMatches || ratingMatches;
      });
      setFilteredCourses(filtered);
    };
  
    filterCourses();
  }, [searchQuery, courses]);
  const handleNext = () => {
    setStartIndex((prevIndex) => prevIndex + 4);
  };

  const handlePrevious = () => {
    setStartIndex((prevIndex) => Math.max(0, prevIndex - 4));
  };

  const visibleCourses = filteredCourses.slice(startIndex, startIndex + 4);

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          mt: 8,
          position: 'relative',
          backgroundImage: `linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url(${logoImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          minHeight: '100vh',
        }}
      >
        <Title>Welcome to Poodle E-Learning!</Title>
        <nav style={{ marginTop: '4rem' }}>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginTop: '1rem' }}>
              <Button component={Link} to="/login" variant="contained" color="primary">
                Login
              </Button>
            </li>
            <li style={{ marginTop: '1rem' }}>
              <Button component={Link} to="/signup" variant="contained" color="primary">
                Signup
              </Button>
            </li>
          </ul>
        </nav>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '2rem' }}>
          <SubTitle>Check out some of our free courses below:</SubTitle>
          <Box mt={4} pr={4}>
            <SearchContainer>
              <SearchIconContainer>
                <SearchOutlined />
              </SearchIconContainer>
              <SearchInput placeholder="Search..." value={searchQuery} onChange={handleSearch} />
            </SearchContainer>
          </Box>
          <Box mt={4} display="flex" justifyContent="center" alignItems="center" gap="1rem">
            <ArrowBackIcon
              color="primary"
              fontSize="large"
              disabled={startIndex === 0}
              onClick={handlePrevious}
              style={{ cursor: 'pointer' }}
            />
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
              {error ? (
                <p>Error fetching courses: {error}</p>
              ) : (
                visibleCourses.map((course) => <CourseCard key={course.id} course={course} />)
              )}
            </div>
            <ArrowForwardIcon
              color="primary"
              fontSize="large"
              disabled={startIndex + 4 >= filteredCourses.length}
              onClick={handleNext}
              style={{ cursor: 'pointer' }}
            />
          </Box>
        </div>
      </Box>
    </>
  );

              }; 
export default HomePage;
