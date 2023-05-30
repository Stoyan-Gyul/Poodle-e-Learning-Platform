import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Box, Button, Container, IconButton, TextField, FormControl, InputLabel, Select, MenuItem, Typography,} from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { Header, LogoImage } from './common.js';
import { createCourse } from './API_requests';

const CreateCoursePage = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('active');
  const [visibility, setVisibility] = useState('public');
  const [expertiseArea, setExpertiseArea] = useState('');
  const [objective, setObjective] = useState('');
  const [error, setError] = useState('');

  const handleCreateCourse = async () => {
    // Check if all fields are filled in
    if (!title || !description || !expertiseArea || !objective) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      const owner_id = 58;
      const courseData = {
        title,
        description,
        owner_id,
        is_active: status,
        is_premium: visibility,
        expertise_area: expertiseArea,
        objective,
      };

      await createCourse(courseData);

      // Course creation successful
      console.log('Course created successfully!');
      // You can redirect to a success page or perform any other actions here
    } catch (error) {
      // Handle any errors that occurred during course creation
      console.error('Error occurred while creating the course:', error);
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
          <IconButton component={Link} to="/dashboard" sx={{ marginBottom: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" component="h2" align="center" gutterBottom>
            Create New Course
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Title"
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              label="Description"
              multiline
              rows={4}
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <FormControl>
              <InputLabel shrink>Status</InputLabel>
              <Select value={status} onChange={(e) => setStatus(e.target.value)}>
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="hidden">Hidden</MenuItem>
              </Select>
            </FormControl>
            <FormControl>
              <InputLabel shrink>Visibility</InputLabel>
              <Select value={visibility} onChange={(e) => setVisibility(e.target.value)}>
                <MenuItem value="public">Public</MenuItem>
                <MenuItem value="premium">Premium</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Expertise Area"
              type="text"
              required
              value={expertiseArea}
              onChange={(e) => setExpertiseArea(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              label="Objective"
              multiline
              rows={4}
              required
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <Button variant="contained" color="primary" size="large" fullWidth onClick={handleCreateCourse}>
              Create Course
            </Button>
            {error && (
              <Typography variant="body1" component="p" color="error" align="center">
                {error}
              </Typography>
            )}
          </Box>
        </Box>
      </Container>
    </>
  );
};

export default CreateCoursePage;

