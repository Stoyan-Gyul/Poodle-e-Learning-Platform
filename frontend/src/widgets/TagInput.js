import React, { useState } from 'react';
import { TextField, Chip, Box } from '@mui/material';

const TagInput = ({ label, onTagsChange }) => {
  const [tags, setTags] = useState([]);
  const [inputValue, setInputValue] = useState('');

  
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      if (inputValue.trim() !== '') {
        const updatedTags = [...tags, inputValue.trim()];
        setTags(updatedTags);
        onTagsChange(updatedTags); // Call the function with updated tags
        setInputValue('');
      }
    }
  };

  const handleDelete = (tag) => {
    const updatedTags = tags.filter((t) => t !== tag);
    setTags(updatedTags);
    onTagsChange(updatedTags); // Call the function with updated tags
  };

  return (
    <Box>
      <TextField
        label={label}
        variant="outlined"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        fullWidth
      />
      <Box mt={1}>
        {tags.map((tag) => (
          <Chip
            key={tag}
            label={tag}
            onDelete={() => handleDelete(tag)}
            variant="outlined"
            color="primary"
            style={{ margin: '0.5rem' }}
          />
        ))}
      </Box>
    </Box>
  );
};

export default TagInput;
