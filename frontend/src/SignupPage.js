import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Box, Button, Container, IconButton, FormControl, MenuItem, Select, TextField, Typography } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { Header, LogoImage } from './common.js';
import { signup, apiLogin } from './API_requests';
import { AuthContext } from './AuthContext';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [first_name, setfirst_name] = useState('');
  const [last_name, setLastName] = useState('');
  const [role, setRole] = useState('student'); // Default role is 'student'
  const [phone, setPhone] = useState('');
  const [linkedin, setLinkedin] = useState('');
  const [error, setError] = useState('');

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };
  const { setAuthToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSignup = async () => {
    // Check if all fields are filled in
    if (!email || !password || !first_name || !last_name || !role) {
      setError('Please fill in all required fields.');
      return;
    }
  
    // Additional validation based on role
    if (role === 'teacher' && (!phone || !linkedin)) {
      setError('Please fill in all required fields.');
      return;
    }
  
    try {
      await signup({
        email,
        password,
        first_name,
        last_name,
        role,
        phone: role === 'teacher' ? phone : undefined,
        linkedin: role === 'teacher' ? linkedin : undefined,
      });
  
      // Signup successful
      const token = await apiLogin(email, password);
  
      // Save the token to local storage
      localStorage.setItem('authToken', token);
  
      // Set the token in the app state
      setAuthToken(token);
  
      // Redirect to Dashboard
      navigate('/dashboard');

    } catch (error) {
      // Handle any network or server errors
      console.error('Error occurred while signing up:', error);
      setError('Signup failed');
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
            Sign Up
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              label="Password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <TextField
              label="First Name"
              type="text"
              required
              value={first_name}
              onChange={(e) => setfirst_name(e.target.value)}
            />
            <TextField
              label="Last Name"
              type="text"
              required
              value={last_name}
              onChange={(e) => setLastName(e.target.value)}
            />
            <FormControl>
              <Select value={role} onChange={handleRoleChange}>
                <MenuItem value="student">Student</MenuItem>
                <MenuItem value="teacher">Teacher</MenuItem>
              </Select>
            </FormControl>
            {role === 'teacher' && (
              <>
                <TextField
                  label="Phone"
                  type="text"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
                <TextField
                  label="LinkedIn"
                  type="text"
                  required
                  value={linkedin}
                  onChange={(e) => setLinkedin(e.target.value)}
                />
              </>
            )}
            <Button variant="contained" color="primary" size="large" fullWidth onClick={handleSignup}>
              Sign Up
            </Button>
            {error && (
              <Typography variant="body1" component="p" color="error" align="center">
                {error}
              </Typography>
            )}
          </Box>
          <Typography variant="body1" component="p" align="center">
            Already have an account? <Link to="/login">Log in</Link>
          </Typography>
        </Box>
      </Container>
    </>
  );
};

export default SignupPage;