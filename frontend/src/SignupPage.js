import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Box, Button, Container, FormControl, MenuItem, Select, TextField, Typography } from '@mui/material';
import { styled } from '@mui/system';

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
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [role, setRole] = useState('student'); // Default role is 'student'
  const [phone, setPhone] = useState('');
  const [linkedin, setLinkedin] = useState('');

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  const handleSignup = () => {
    // Perform signup logic here
    // You can access the values entered by the user in the state variables (email, password, firstName, lastName, role, phone, linkedin)
  };

  const showTeacherFields = role === 'teacher';

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Container maxWidth="sm">
        <Box sx={{ mt: 15 }}>
          <Typography variant="h4" component="h2" align="center" gutterBottom>
            Signup
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
            <TextField
              label="First Name"
              type="text"
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
            <TextField
              label="Last Name"
              type="text"
              required
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
            />
            <FormControl fullWidth>
              <Select value={role} onChange={handleRoleChange} displayEmpty>
                <MenuItem value="student">Student</MenuItem>
                <MenuItem value="teacher">Teacher</MenuItem>
              </Select>
            </FormControl>
            {showTeacherFields && (
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
              Signup
            </Button>
          </Box>
          <Typography variant="body1" component="p" align="center">
            Already have an account? <Link to="/login">Login</Link>
          </Typography>
        </Box>
      </Container>
    </>
  );
};

export default SignupPage;





