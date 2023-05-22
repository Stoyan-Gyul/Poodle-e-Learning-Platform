import React from 'react';
import Box from '@mui/material/Box';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import { styled } from '@mui/system';

import logoImage from './images/logo.png'; // Assuming your logo image file is named 'logo.png' and located in the 'images' folder within your 'src' folder

const Title = styled('h1')({
  fontSize: '2rem',
  background: 'linear-gradient(to right, rgb(216, 0, 132), rgb(255, 132, 0), rgb(255, 216, 0), rgb(0, 128, 255), #7d68a1)',
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
  borderTop: '1px solid #7d68a1', // Replace with your desired line color
});

const LogoImage = styled('img')({
  width: '50px',
  height: '50px',
  borderRadius: '50%',
});

const HomePage = () => {
  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 8, position: 'relative' }}>
        <Title>
          Welcome to Poodle E-Learning!
        </Title>
        <nav style={{ marginTop: '4rem' }}> {/* Adjust this value to control the distance between the title and buttons */}
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginTop: '1rem' }}> {/* Adjust this value to control the spacing between the buttons */}
              <StyledButton component={Link} to="/login" variant="contained" color="primary">
                Login
              </StyledButton>
            </li>
            <li style={{ marginTop: '1rem' }}> {/* Adjust this value to control the spacing between the buttons */}
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


