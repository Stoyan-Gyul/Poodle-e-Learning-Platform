import React, { useState, useEffect, useContext } from 'react';
import { Box, Container, Typography, IconButton, TextField, Button, Grid } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import logoImage from './images/logo.png';
import { LogoImage, Header, LogoutButton } from './common.js';
import { AuthContext } from './AuthContext';

const ProfilePage = () => {
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [linked_in_account, setlinked_in_account] = useState('');
  const [isEditMode, setIsEditMode] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [userRole, setUserRole] = useState('');
  const { logout } = useContext(AuthContext);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`,
          },
        });

        if (response.ok) {
          const currentUser = await response.json();

          setFirstName(currentUser.first_name);
          setLastName(currentUser.last_name);
          setPhone(currentUser.phone);
          setlinked_in_account(currentUser.linked_in_account);
          setUserRole(currentUser.role);
        } else {
          console.error('Failed to fetch user data', response);
          setErrorMessage('Failed to fetch user data');
        }
      } catch (error) {
        console.error('Failed to fetch user data', error);
        setErrorMessage('Failed to fetch user data');
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const handleEditMode = () => {
    setIsEditMode(true);
    setPassword(''); // Clear the password field when entering edit mode
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();

    // Retrieve the authentication token from local storage
    const authToken = localStorage.getItem('authToken');


    try {
      // Make the API request to update the profile
      const response = await fetch('http://localhost:8000/users/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`, // Include the authentication token in the header
        },
        body: JSON.stringify({
          password: password !== '' ? password : undefined, // Only include the password if it's not empty
          first_name,
          last_name,
          phone,
          linked_in_account,
        }),
      });

      if (response.ok) {
        setSuccessMessage('Profile updated successfully!');
        setErrorMessage('');
      } else {
        setSuccessMessage('');
        setErrorMessage('Failed to update profile');
      }
    } catch (error) {
      console.error('Failed to update profile', error);
      setSuccessMessage('');
      setErrorMessage('Failed to update profile');
    }

    setIsEditMode(false);
  };

  const renderPasswordField = () => {
    if (isEditMode) {
      return (
        <Grid item xs={12}>
          <TextField
            label="Password"
            type="password"
            fullWidth
            disabled={!isEditMode}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Grid>
      );
    }

    return (
      <Grid item xs={12}>
        <TextField
          label="Password"
          type="password"
          fullWidth
          disabled={!isEditMode}
          value="*******"
          InputProps={{ readOnly: true }}
        />
      </Grid>
    );
  };

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
          </a>
        <div style={{ marginLeft: 'auto' }}>
        <LogoutButton>Logout</LogoutButton>
        </div>
      </Header>
      <div style={{ marginTop: '64px' }}> {/* Adjust the margin value as needed */}
        <Container maxWidth="sm">
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
            <IconButton component={Link} to="/dashboard">
              <ArrowBack />
            </IconButton>
            <Typography variant="h4" component="h1" align="center" style={{ flex: '1', marginLeft: '16px' }}>
              Profile
            </Typography>
          </div>
          <form onSubmit={handleSaveProfile}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  label="First Name"
                  fullWidth
                  disabled={!isEditMode}
                  value={first_name}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Last Name"
                  fullWidth
                  disabled={!isEditMode}
                  value={last_name}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </Grid>
              {renderPasswordField()}
              {userRole === 'teacher' && (
                <>
                  <Grid item xs={12}>
                    <TextField
                      label="Phone"
                      fullWidth
                      disabled={!isEditMode}
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      label="Linked Account"
                      fullWidth
                      disabled={!isEditMode}
                      value={linked_in_account}
                      onChange={(e) => setlinked_in_account(e.target.value)}
                    />
                  </Grid>
                </>
              )}
              {!isEditMode && (
                <Grid item xs={12}>
                  <Button variant="contained" color="primary" fullWidth onClick={handleEditMode}>
                    Edit Profile
                  </Button>
                </Grid>
              )}
              {isEditMode && (
                <Grid item xs={12}>
                  <Button type="submit" variant="contained" color="primary" fullWidth>
                    Save Profile
                  </Button>
                </Grid>
              )}
            </Grid>
          </form>
          {successMessage && (
            <Typography variant="body1" component="p" color="success" align="center">
              {successMessage}
            </Typography>
          )}
          {errorMessage && (
            <Typography variant="body1" component="p" color="error" align="center">
              {errorMessage}
            </Typography>
          )}
        </Container>
      </div>
    </>
  );
};

export default ProfilePage;

