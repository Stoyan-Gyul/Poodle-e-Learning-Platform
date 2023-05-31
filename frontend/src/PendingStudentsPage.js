import React, { useEffect, useState } from 'react';
import { Typography, Paper, Button, IconButton } from '@mui/material';
import { Link } from 'react-router-dom';
import { ArrowBack } from '@mui/icons-material';
import { Header, LogoImage } from './common.js';
import logoImage from './images/logo.png';
import { fetchPendingApprovalsForStudents, handleApproveEnrollment } from './API_requests.js';

const PendingStudentsPage = () => {
  const [pendingApprovals, setPendingApprovals] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const pendingApprovalsData = await fetchPendingApprovalsForStudents(localStorage.user_id);
        setPendingApprovals(pendingApprovalsData);
      } catch (error) {
        console.error('Error fetching pending approvals:', error);
      }
    };

    fetchData();
  }, []);

  const handleApproveClick = async (approval) => {
    try {
      await handleApproveEnrollment(approval.user_id, approval.course_id);
      // Perform any additional actions after approval
      console.log('Enrollment approved:', approval);
    } catch (error) {
      console.error('Error approving enrollment:', error);
    }
  };

  return (
    <>
      <Header>
        <a href="/">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
    
      <div style={{ marginTop: '6rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
          <IconButton component={Link} to="/dashboard">
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="h1" align="center" gutterBottom>
            Pending Students
          </Typography>
        </div>
        {pendingApprovals.map((approval) => (
          <Paper
            key={approval.user_id}
            elevation={3}
            sx={{
              p: 2,
              margin: '1rem auto',
              width: '80%',
              maxWidth: '800px',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <Typography variant="body1" sx={{ flex: '1 1 auto' }} gutterBottom>
              Student {approval.user_first_name} {approval.user_last_name} has requested enrollment in your class {approval.course_title}.
            </Typography>
            <Button variant="contained" onClick={() => handleApproveClick(approval)}>
              Approve
            </Button>
          </Paper>
        ))}
      </div>
    </>
  );
};

export default PendingStudentsPage;






