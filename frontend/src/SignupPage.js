import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Box, Button, Container, FormControl, MenuItem, Select, TextField, Typography } from '@mui/material';
import { styled } from '@mui/system';
import { AuthContext } from './AuthContext';
import logoImage from './images/logo.png';

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
  borderTop: '1px solid #7d68a1',
});

const LogoImage = styled('img')({
  width: '50px',
  height: '50px',
  borderRadius: '50%',
});

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [first_name, setfirst_name] = useState('');
  const [last_name, setLastName] = useState('');
  const [role, setRole] = useState('student'); // Default role is 'student'
  const [phone, setPhone] = useState('');
  const [linkedin, setLinkedin] = useState('');
  const [error] = useState('');

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };
  const { setAuthToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const userData = {
        email,
        password,
        first_name,
        last_name,
        role,
      };

      if (role === 'teacher') {
        userData.phone = phone;
        userData.linkedin = linkedin;
      }

      const response = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        // Signup successful
        await handleLogin();
      } else {
        // Signup failed
        // You can handle the error and display an appropriate message to the user
        console.log('Signup failed');
      }
    } catch (error) {
      // Handle any network or server errors
      console.error('Error occurred while signing up:', error);
    }
  };

  const handleLogin = async () => {
    try {
      // Make the API request and get the token
      const loginResponse = await fetch('http://localhost:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (loginResponse.ok) {
        // Login successful
        const { token } = await loginResponse.json();

        // Set the token in the app state or local storage
        // For example, if you have a state management library like Redux, you can dispatch an action to set the token
        // Or if you want to store it in local storage, you can use: localStorage.setItem('token', token);
        setAuthToken(token);

        // Redirect to Dashboard
        navigate('/dashboard');
      } else {
        // Login failed
        console.log('Login failed');
      }
    } catch (error) {
      // Handle any network or server errors
      console.error('Error occurred while logging in:', error);
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