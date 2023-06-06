import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Box, Button, Container, IconButton, TextField, FormControl, InputLabel, Select, MenuItem, Typography, } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import logoImage from './images/logo.png';
import { Header, LogoImage } from './common.js';
import { createCourse, uploadPicToCourse } from './API_requests';
import TagInput from './widgets/TagInput';

const CreateCoursePage = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('active');
  const [visibility, setVisibility] = useState('public');
  
  const [picFile, setPicFile] = useState(null);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [area, setArea] = useState([]);
  const [objectives, setObjectives] = useState([]);

  const handleAreaChange = (tags) => {
    setArea(tags);
  };

  const handleObjChange = (tags) => {
    setObjectives(tags);
  };

  const handleCreateCourse = async () => {
    // Check if all fields are filled in
    if (!title || !description || !area || !objectives) {
      setError('Please fill in all required fields.');
      return;
    }
    console.log('area:', area);
    console.log('objectives:', objectives);
    try {
  
      const courseData = {
        title,
        description,
        owner_id: localStorage.getItem('user_id'),
        is_active: status,
        is_premium: visibility,
        tags: area,
        objectives: objectives,
      };

      const response = await createCourse(courseData);

      const courseId = response.id;
      await uploadPicToCourse(courseId, picFile);

      // Course creation successful
      console.log('Course created successfully!');

      setSuccessMessage('Course created successfully!');

    } catch (error) {
      // Handle any errors that occurred during course creation
      console.error('Error occurred while creating the course:', error);
    }
  };


  const handlePicFileChange = (event) => {
    const file = event.target.files[0];
    setPicFile(file);
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

            <TagInput label="Tags" onTagsChange={handleAreaChange} />

            <TagInput label="Objectives" onTagsChange={handleObjChange} />
            
            <input type="file" accept="image/*" onChange={handlePicFileChange} />
            <Button variant="contained" color="primary" size="large" fullWidth onClick={handleCreateCourse}>
              Create Course
            </Button>
            {error && (
              <Typography variant="body1" component="p" color="error" align="center">
                {error}
              </Typography>
            )}
            {successMessage && (
              <Box
                sx={{
                  backgroundColor: '#e6f7f2',
                  padding: '8px',
                  borderRadius: '4px',
                  display: 'flex',
                  justifyContent: 'center',
                }}
              >
                <Typography variant="body1" component="p" color="success">
                  {successMessage}
                </Typography>
              </Box>
            )}
          </Box>
        </Box>
      </Container>
    </>
  );

};

export default CreateCoursePage; 
