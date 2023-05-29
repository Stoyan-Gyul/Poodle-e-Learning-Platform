import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Box, Button, Container, IconButton, TextField, Typography } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { AuthContext } from './AuthContext';
import logoImage from './images/logo.png'; // Import your logo image
import { Header, LogoImage } from './common.js';

const LoginPage = () => {
  const { setAuthToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Email and password cannot be empty.');
      return;
    }
  
    try {
      // Make the API request and get the token
      const token = await apiLogin(email, password);
  
      // Save the token to local storage
      localStorage.setItem('authToken', token);
  
      // Set the token in the app state
      setAuthToken(token);
  
      // Redirect to Dashboard
      navigate('/dashboard');
    } catch (error) {
      setError('Login failed. Please check your email and password.');
      console.error(error);
    }
  };  

  // API login function
  const apiLogin = async (email, password) => {
    // Make the POST request to your backend API
    const response = await fetch('http://localhost:8000/users/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      const token = data.token;
      return token;
    } else {
      throw new Error('Login failed');
    }
  };

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Container maxWidth="sm">
        <Box sx={{ mt: 8 }}>
          <IconButton component={Link} to="/" sx={{ marginBottom: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" component="h2" align="center" gutterBottom>
            Login
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField label="Email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
            <TextField
              label="Password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button variant="contained" color="primary" size="large" fullWidth onClick={handleLogin}>
              Login
            </Button>
            {error && (
              <Typography variant="body1" component="p" color="error" align="center">
                {error}
              </Typography>
            )}
          </Box>
          <Typography variant="body1" component="p" align="center">
            Don't have an account? <Link to="/signup">Sign up</Link>
          </Typography>
        </Box>
      </Container>
    </>
  );
};

export default LoginPage;



