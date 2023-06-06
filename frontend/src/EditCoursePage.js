import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Typography, Box, Container, Card, CardContent, TextField, Button, IconButton, Chip, MenuItem, Stack } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';

import logoImage from './images/logo.png';
import { Header, LogoImage } from './common.js';
import { fetchCourseData, handleUpdateCourse } from './API_requests.js';


const EditCoursePage = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [formData, setFormData] = useState({}); // Store form data
  const { is_active, is_premium } = formData;
  const [error] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const courseData = await fetchCourseData(courseId);
        setCourse(courseData);
        setIsLoading(false);
        setFormData({
          title: courseData.title,
          description: courseData.description,
          is_active: courseData.is_active ? 'active' : 'hidden',
          is_premium: courseData.is_premium ? 'premium' : 'public',
          tags: courseData.tags,
          objectives: courseData.objectives,
        });
      } catch (error) {
        console.error('Error fetching course data:', error);
        setIsLoading(false);
      }
    };

    fetchCourse();
  }, [courseId]);

  const handleInputChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const updateCourse = async (event) => {
    event.preventDefault();

    // Validate form fields
    if (
      !formData.title ||
      !formData.description ||
      !formData.is_active ||
      !formData.is_premium ||
      formData.tags.length === 0 ||
      formData.objectives.length === 0
    ) {
      console.error('Please fill in all the necessary fields');
      return;
    }


    // Create updated data object with only the changed values
    const updatedData = {
      title: formData.title,
      description: formData.description,
      is_active: is_active ? 'active' : 'hidden',
      is_premium: is_premium ? 'premium' : 'public',
      tags: formData.tags,
      objectives: formData.objectives,
    };
    console.log(updatedData)
    try {
      await handleUpdateCourse(courseId, updatedData);
      console.log('Course updated successfully');
      setSuccessMessage('Course updated successfully!')

    } catch (error) {
      console.error('Error updating course:', error);
    }
  };


  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!course) {
    return <div>Course not found.</div>;
  }

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
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
            <Card sx={{ width: '500px', boxShadow: 2 }}>
              <CardContent>
                <Typography variant="h4" component="h1" gutterBottom>
                  Edit Course: {course.title}
                </Typography>
                <Box component="form" onSubmit={updateCourse} sx={{ mt: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Course Details
                  </Typography>
                  <TextField
                    name="title"
                    label="Title"
                    value={formData.title || ''}
                    onChange={handleInputChange}
                    fullWidth
                    required
                    sx={{ mt: 1 }}
                  />
                  <TextField
                    name="description"
                    label="Description"
                    value={formData.description || ''}
                    onChange={handleInputChange}
                    fullWidth
                    required
                    multiline
                    rows={4}
                    sx={{ mt: 1 }}
                  />
                  <TextField
                    select
                    name="is_active"
                    label="Status"
                    value={formData.is_active === 'active' ? true : false}
                    onChange={handleInputChange}
                    fullWidth
                    sx={{ mt: 1 }}
                  >
                    <MenuItem value={true}>Active</MenuItem>
                    <MenuItem value={false}>Hidden</MenuItem>
                  </TextField>

                  <TextField
                    select
                    name="is_premium"
                    label="Visibility"
                    value={formData.is_premium === 'premium' ? true : false}
                    onChange={handleInputChange}
                    fullWidth
                    sx={{ mt: 2 }}
                  >
                    <MenuItem value={true}>Premium</MenuItem>
                    <MenuItem value={false}>Public</MenuItem>
                  </TextField>

                  <Box sx={{ mt: 1 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Tags:
                    </Typography>
                    <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                      {formData.tags &&
                        formData.tags.map((tag) => (
                          <Chip
                            key={tag}
                            label={tag}
                            variant="outlined"
                            color="primary"
                          />
                        ))}
                    </Stack>
                  </Box>

                  <Box sx={{ mt: 1 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Objectives:
                    </Typography>
                    <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                      {formData.objectives &&
                        formData.objectives.map((objective) => (
                          <Chip
                            key={objective}
                            label={objective}
                            variant="outlined"
                            color="primary"
                          />
                        ))}
                    </Stack>
                  </Box>

                  <Button type="submit" variant="contained" sx={{ mt: 2 }}>
                    Save
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
              </CardContent>
            </Card>
          </Box>
        </Box>
      </Container>
    </>
  );
};

export default EditCoursePage
