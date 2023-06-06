import logoImage from './images/logo.png';
import { Header, LogoImage } from './common.js';
import { fetchAllSectionsForCourse, fetchCourseData } from './API_requests';

import React, { useEffect, useState } from 'react';
import { Typography, Box, Card, List, ListItem, ListItemButton, ListItemText, Checkbox, IconButton } from '@mui/material';
import { ArrowBack, AddCircleOutline } from '@mui/icons-material';
import { Link, useParams } from 'react-router-dom';

const SectionsPage = () => {
  const [course, setCourse] = useState(null);
  const [sections, setSections] = useState([]);
  const { courseId } = useParams();
  const userRole = localStorage.getItem('role'); // Retrieve the role from local storage

  useEffect(() => {
    const fetchData = async () => {
      try {
        const courseData = await fetchCourseData(courseId);
        const sectionsData = await fetchAllSectionsForCourse(courseId);
        setCourse(courseData);
        setSections(sectionsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [courseId]);

  const handleToggle = (sectionId) => () => {
    setSections((prevSections) =>
      prevSections.map((section) =>
        section.id === sectionId ? { ...section, checked: !section.checked } : section
      )
    );
  };

  return (
    <>
      <Header>
        <a href="/dashboard">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box display="flex" justifyContent="center" marginTop={8}>
        <IconButton component={Link} to="/dashboard" sx={{ marginRight: 170 }}>
          <ArrowBack />
        </IconButton>
        {userRole === 'teacher' && (
          <IconButton component={Link} to={`/${courseId}/new-section`}>
            <AddCircleOutline />
          </IconButton>
        )}
      </Box>
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="40vh">
        {course && (
          <Box textAlign="center">
            <Typography variant="h3" component="h3" gutterBottom>
              Sections for Course: {course.title}
            </Typography>
            <Box width="50%" maxWidth={500} margin="auto">
              <Card style={{ width: '100%', height: '100%' }}>
                <img
                  src={`data:image/jpeg;base64,${course.home_page_pic}`}
                  alt="Course Pic Not Available"
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </Card>
            </Box>
          </Box>
        )}
        <List>
          {sections.map((section) => (
            <ListItem key={section.id} disablePadding>
              <ListItemButton onClick={handleToggle(section.id)}>
                <ListItemText
                  primaryTypographyProps={{ variant: 'h4' }}
                  primary={`Section: ${section.title}`}
                />
                <Checkbox checked={section.checked} edge="end" />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </>
  );
};

export default SectionsPage;
