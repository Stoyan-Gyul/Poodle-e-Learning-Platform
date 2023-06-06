import React, { useState } from 'react';
import { TextField, Button, Typography, Box, IconButton } from '@mui/material';
import { useParams } from 'react-router-dom';
import { ArrowBack } from '@mui/icons-material';
import { Link } from 'react-router-dom';

import { LogoImage, Header } from './common.js';
import logoImage from './images/logo.png';
import { createSection } from './API_requests';

const CreateSectionPage = () => {
    const { courseId } = useParams();
    const [sectionData, setSectionData] = useState({
        title: '',
        content: '',
        description: '',
        external_link: ''
    });
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setSectionData((prevSectionData) => ({
            ...prevSectionData,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const result = await createSection(courseId, sectionData);

            if (result.success) {
                setSuccessMessage(result.message);
                setErrorMessage('');
                setSectionData({
                    title: '',
                    content: '',
                    description: '',
                    external_link: ''
                });
            } else {
                setErrorMessage(result.message);
                setSuccessMessage('');
            }
        } catch (error) {
            console.error('Error creating section:', error);
            setErrorMessage('Error creating section');
            setSuccessMessage('');
        }
    };

    return (
        <><Header>
        <a href="/dashboard">
          <LogoImage src={logoImage} alt="Logo" />
        </a>
      </Header>
      <Box display="flex" justifyContent="center" marginTop={8}>
        <IconButton component={Link} to="/dashboard" sx={{ marginRight: 170 }}>
          <ArrowBack />
        </IconButton>
      </Box>
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="70vh">
            <Typography variant="h4" component="h4" gutterBottom>
                Create New Section
            </Typography>
            <Box width="50%" maxWidth={500} marginX="auto">
                <form onSubmit={handleSubmit}>
                    <TextField
                        name="title"
                        label="Title"
                        value={sectionData.title}
                        onChange={handleInputChange}
                        required
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="content"
                        label="Content"
                        value={sectionData.content}
                        onChange={handleInputChange}
                        multiline
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="description"
                        label="Description"
                        value={sectionData.description}
                        onChange={handleInputChange}
                        required
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="external_link"
                        label="External Link"
                        value={sectionData.external_link}
                        onChange={handleInputChange}
                        required
                        fullWidth
                        margin="normal"
                    />
                    <Button type="submit" variant="contained" color="primary" fullWidth>
                        Create Section
                    </Button>
                </form>
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
        </>
    );
};

export default CreateSectionPage;
