import CheckCircleIcon from '@mui/icons-material/CheckCircle';

import React, { useEffect, useState } from 'react';
import { Typography, Box, CircularProgress, Paper, IconButton } from '@mui/material';
import { useParams, Link } from 'react-router-dom';
import { fetchReportByCourseId } from './API_requests.js';
import logoImage from './images/logo.png';
import { ArrowBack, Person as PersonIcon, Star as StarIcon, Timer as TimerIcon, Checklist as ChecklistIcon, CheckCircleOutline as CheckCircleOutlineIcon } from '@mui/icons-material';
import { Header, LogoImage } from './common.js';

const CourseReportPage = () => {
  const { courseId } = useParams();
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchReports = async () => {
    try {
      const response = await fetchReportByCourseId(courseId);
      setReports(response);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box sx={{ flexGrow: 1, marginTop: '4rem', textAlign: 'left' }}>
        <IconButton component={Link} to="/courses">
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" component="h1" align="center" gutterBottom>
          Report for Course: {reports.length > 0 ? reports[0].title : ''}
        </Typography>

        {isLoading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="200px">
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {reports.length === 0 ? (
              <Typography variant="body1" align="center">
                No reports found for this course.
              </Typography>
            ) : (
              reports.map((report, index) => (
                <Box key={index} sx={{ marginBottom: '1rem', textAlign: 'center' }}>
                  <Paper elevation={3} sx={{ width: '20rem', padding: '1rem', display: 'inline-block' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <PersonIcon sx={{ marginRight: '0.5rem', fontSize: 20 }} />
                      <Typography variant="body1">
                        <strong>Student:</strong> {report.first_name} {report.last_name}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <StarIcon sx={{ marginRight: '0.5rem', fontSize: 20 }} />
                      <Typography variant="body1">
                        <strong>Rating:</strong> {report.rating}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <CheckCircleOutlineIcon sx={{ marginRight: '0.5rem', fontSize: 20 }} />
                      <Typography variant="body1">
                        <strong>Status:</strong> {report.status}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <ChecklistIcon sx={{ marginRight: '0.5rem', fontSize: 20 }} />
                      <Typography variant="body1">
                        <strong>Progress:</strong> {report.progress}
                      </Typography>
                    </Box>
                  </Paper>
                </Box>
              ))
            )}
          </Box>
        )}
      </Box>
    </>
  );
};

export default CourseReportPage;

