import React from 'react';
import { Grid, Box, Typography, IconButton, InputBase, Avatar, Menu, MenuItem } from '@mui/material';
import { styled } from '@mui/system';
import { HomeOutlined, PersonOutlined, BookOutlined, SearchOutlined } from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';

import logoImage from './images/logo.png'; // Assuming your logo image file is named 'logo.png' and located in the 'images' folder within your 'src' folder

const LogoIcon = styled(Avatar)(({ theme }) => ({
  width: theme.spacing(8),
  height: theme.spacing(8),
  marginBottom: theme.spacing(2), // Add margin bottom to create space between the logo icon and the menu items
}));

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

const SearchInput = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  padding: theme.spacing(1, 1, 1, 0),
  paddingLeft: `calc(1em + ${theme.spacing(4)})`,
  transition: theme.transitions.create('width'),
}));

const VerticalLine = styled('div')(({ theme }) => ({
  borderRight: `1px solid ${theme.palette.divider}`,
  height: '100%',
  position: 'absolute',
  top: 0,
  left: '20',
  transform: 'translateX(-50%)',
}));

const Dashboard = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    navigate('/profile');
    handleMenuClose();
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container>
        {/* Left Section */}
        <Grid item xs={2.5}>
          <Box textAlign="center" mt={4} ml={13}>
            <LogoIcon alt="Logo Icon" src={logoImage} /> {/* Use the imported logo image */}
          </Box>
          <Box mt={4}>
            <Box mb={2}>
              <MenuItem 
                onClick={handleMenuClose}
                component={Link} // Add Link component to enable navigation
                to="/"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: 'pink',
                  },
                }}
              >
                <IconButton>
                  <HomeOutlined />
                </IconButton>
                Home
              </MenuItem>
            </Box>
            <Box mb={2}>
              <MenuItem 
                onClick={handleProfileClick} // Call handleProfileClick on click event
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: 'pink',
                  },
                }}
              >
                <IconButton>
                  <PersonOutlined />
                </IconButton>
                Profile
              </MenuItem>
            </Box>
            <Box>
              <MenuItem 
                onClick={handleMenuClose}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: '20px',
                  '&:hover': {
                    backgroundColor: 'pink',
                  },
                }}
              >
                <IconButton>
                  <BookOutlined />
                </IconButton>
                Courses
              </MenuItem>
            </Box>
          </Box>
        </Grid>

        {/* Vertical Line */}
        <Grid item xs={1}>
          <VerticalLine />
        </Grid>

        {/* Right Section */}
        <Grid item xs={8}>
          <Box display="flex" justifyContent="flex-end" mt={4} pr={4}>
            <SearchContainer>
              <SearchIconContainer>
                <SearchOutlined />
              </SearchIconContainer>
              <SearchInput placeholder="Search..." />
            </SearchContainer>
          </Box>
          <Box mt={4} px={4}>
            {/* Rest of the content in the right section */}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
