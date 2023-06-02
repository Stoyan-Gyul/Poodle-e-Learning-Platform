import React, { useState, useEffect } from 'react';
import { Box, Button, Paper, InputAdornment, TextField } from '@mui/material/';
import { Link } from 'react-router-dom';
import { styled } from '@mui/system';
import { Header, LogoImage } from './common.js';
import { fetchAllCourses } from './API_requests.js';
import logoImage from './images/logo.png';

import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import SearchIcon from '@mui/icons-material/Search';


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

const SearchInput = styled(TextField)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  padding: theme.spacing(1, 1, 1, 0),
  paddingLeft: `calc(1em + ${theme.spacing(4)})`,
  transition: theme.transitions.create('width'),
}));

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
        height: 400,
      }}
    >
      <h3>{course.title}</h3>
      <p>{course.description}</p>
      <p>Expertise Area: {course.expertise_area}</p>
    </Paper>
  );
};

const HomePage = () => {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState('');
  const [startIndex, setStartIndex] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const coursesData = await fetchAllCourses();
        setCourses(coursesData);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setError('Failed to fetch courses');
      }
    };

    fetchData();
  }, []);

  const handleNext = () => {
    setStartIndex((prevIndex) => prevIndex + 4);
  };

  const handlePrevious = () => {
    setStartIndex((prevIndex) => Math.max(0, prevIndex - 4));
  };

  const visibleCourses = courses
  .filter(
    (course) =>
      course.expertise_area.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.ourse_rating.toString().includes(searchTerm)
  )
  .slice(startIndex, startIndex + 4);

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
      <div>
        <TextField
          type="text"
          value={searchTerm}
          onChange={handleSearchChange}
          placeholder="Search by specialization or rating"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
            style: { fontSize: '2rem' },
          }}
          fullWidth
          style={{ marginBottom: '1rem' }}
        />
      </div>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem' }}>
            <ArrowBackIcon
              color="primary"
              fontSize="large"
              disabled={startIndex === 0}
              onClick={handlePrevious}
              style={{ cursor: 'pointer' }}
            />
            {error ? (
              <p>Error fetching courses: {error}</p>
            ) : (
              visibleCourses.map((course) => <CourseCard key={course.id} course={course} />)
            )}
            <ArrowForwardIcon
              color="primary"
              fontSize="large"
              disabled={startIndex + 4 >= courses.length}
              onClick={handleNext}
              style={{ cursor: 'pointer' }}
            />
          </div>
        </div>
      </Box>
    </>
  );
};

export default HomePage;
