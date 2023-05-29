import React from 'react';
import Box from '@mui/material/Box';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import { styled } from '@mui/system';
import { Header, LogoImage } from './common.js';

import logoImage from './images/logo.png'; // Assuming your logo image file is named 'logo.png' and located in the 'images' folder within your 'src' folder

const Title = styled('h1')({
  fontSize: '5rem',
  background: '#1976d2',
  WebkitTextFillColor: 'transparent',
  '-webkit-background-clip': 'text',
  '-moz-background-clip': 'text',
  display: 'inline-block',
  margin: '3rem 0 1rem', // Adjust this value to control the distance between the title and buttons
});

const StyledButton = styled(Button)({
  fontSize: '1.2rem',
  marginBottom: '1rem', // Adjust this value to control the spacing between the buttons
});

const HomePage = () => {
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
              <StyledButton component={Link} to="/login" variant="contained" color="primary">
                Login
              </StyledButton>
            </li>
            <li style={{ marginTop: '1rem' }}>
              <StyledButton component={Link} to="/signup" variant="contained" color="primary">
                Signup
              </StyledButton>
            </li>
          </ul>
        </nav>
      </Box>
    </>
  );
};

export default HomePage;

