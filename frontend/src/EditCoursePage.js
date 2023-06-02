import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchCourseData } from './API_requests.js';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const EditCoursePage = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [formData, setFormData] = useState({}); // Store form data

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const courseData = await fetchCourseData(courseId);
        setCourse(courseData);
        setIsLoading(false);
        setFormData(courseData); // Initialize form data with fetched course data
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

  const handleSubmit = (event) => {
    event.preventDefault();
    // Perform form submission logic or API request to update the course data
    console.log(formData);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!course) {
    return <div>Course not found.</div>;
  }

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <Card sx={{ width: '500px', boxShadow: 2 }}>
        <CardContent>
          <Typography variant="h4" component="h1" gutterBottom>
            Edit Course: {course.title}
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
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
              name="objective"
              label="Objective"
              value={formData.objective || ''}
              onChange={handleInputChange}
              fullWidth
              required
              multiline
              rows={4}
              sx={{ mt: 1 }}
            />
            <TextField
              name="is_premium"
              label="Visibility"
              value={formData.is_premium ? 'Premium' : 'Public'}
              disabled
              fullWidth
              sx={{ mt: 1 }}
            />
            <TextField
              name="is_active"
              label="Status"
              value={formData.is_active ? 'Active' : 'Hidden'}
              disabled
              fullWidth
              sx={{ mt: 1 }}
            />
            <TextField
              name="expertise_area"
              label="Expertise Area"
              value={formData.expertise_area || ''}
              onChange={handleInputChange}
              fullWidth
              required
              sx={{ mt: 1 }}
            />
            <Button type="submit" variant="contained" sx={{ mt: 2 }}>
              Save
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EditCoursePage;




