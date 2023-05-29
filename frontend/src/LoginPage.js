import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Box, Button, Container, IconButton, TextField, Typography } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { AuthContext } from './AuthContext';
import { UserContext } from './UserContext';
import logoImage from './images/logo.png'; // Import your logo image
import { Header, LogoImage } from './common.js';
import { apiLogin, viewUserData } from './API_requests';

const LoginPage = () => {
  const { setAuthToken } = useContext(AuthContext);
  const { setUserId, setRole} = useContext(UserContext)
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
      const userData = await viewUserData(token);
      const user_id = userData.id;
      const role = userData.role;
  
      // Save the token to local storage
      localStorage.setItem('authToken', token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('role', role)
  
  
      // Set the token, user_id and rolein the app state
      setAuthToken(token);
      setUserId(user_id); 
      setRole(role); 

      // Redirect to Dashboard
      navigate('/dashboard');
    } catch (error) {
      setError('Login failed. Please check your email and password.');
      console.error(error);
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



