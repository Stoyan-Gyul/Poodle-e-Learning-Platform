import axios from 'axios';

const authToken = localStorage.getItem('authToken');
const user_id = localStorage.getItem('user_id')
const role = localStorage.getItem('role')

export const apiLogin = async (email, password) => {
  // Make the POST request to your backend API
  const response = await fetch('http://localhost:8000/users/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    const token = data.token;
    return token;
  } else {
    throw new Error('Login failed');
  }
};

export const handleLogout = () => {
  // Remove the token from local storage
  localStorage.removeItem('token');
};

export const signup = async (userData) => {
  try {
    const response = await fetch('http://localhost:8000/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      // Signup successful
      return;
    } else {
      // Signup failed
      // Handle the error and throw an appropriate error
      const errorData = await response.json();
      const errorMessage = errorData.detail || 'Signup failed';
      throw new Error(errorMessage);
    }
  } catch (error) {
    // Handle any network or server errors
    console.error('Error occurred while signing up:', error);
    throw new Error('Signup failed');
  }
};

export const viewUserData = async (token) => {
  try { 
    const authorization = `Bearer ${token}`; 

    const response = await fetch('http://localhost:8000/users/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authorization
      },
    });
    if (response.ok) {
      const data = await response.json();
      return data;

    } else {
      const errorData = await response.json();
      const errorMessage = errorData.detail || 'Failed to get user data';
      throw new Error(errorMessage);
    }
  } catch (error) {
    // Handle any network or server errors
    console.error('Error occurred while signing up:', error);
    throw new Error('Failed to get user data');
  }
};


export const handleUnsubscribeFromCourse = async (courseId) => {
    
    try {
      const response = await fetch(`http://localhost:8000/users/${user_id}/courses/${courseId}/unsubscribe`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
    
      if (!response.ok) {
        throw new Error('Failed to unsubscribe from the course');
      }
      
      return response.json();
    } catch (error) {
      console.log('Error unsubscribing from the course:', error);
      throw error;
    }
  };

export const handleSubscribeToCourse = async (courseId) => {

  try {
    const response = await fetch(`http://localhost:8000/users/${user_id}/courses/${courseId}/subscribe`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  
    if (!response.ok) {
      throw new Error('Failed to Subscribe to the course');
    }
    
    return response.json();
  } catch (error) {
    console.log('Error subscribing to the course:', error);
    throw error;
  }

  };

export const fetchCourseData = async (courseId) => {
  try {
    const response = await fetch(`http://localhost:8000/courses/${courseId}`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  
    if (!response.ok) {
      throw new Error(`Failed to fetch course data for course ${courseId}`);
    }
  
    return response.json();
  } catch (error) {
    console.error('Error fetching course data:', error);
    throw error;
  }
};
  
export const fetchEnrolledCourses = async () => {

  try {
    const response = await fetch('http://localhost:8000/courses/enrolled_courses', {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    if (response.status === 401) {
      throw new Error('Please login to view this information.');
    }

    const data = await response.json();

    if (Array.isArray(data)) {
      return data;
    } else {
      return [];
    }
  } catch (error) {
    console.log('Error fetching enrolled courses:', error);
    throw error;
  }
};

export const fetchAllCourses = async () => {
  try {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (authToken) {
      headers.Authorization = `Bearer ${authToken}`;
    }

    const response = await fetch('http://localhost:8000/courses/', {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      throw new Error('Failed to fetch courses');
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching courses:', error);
    throw error;
  }
};


export const createCourse = async (courseData) => {
  try {
    const response = await fetch(`http://localhost:8000/courses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify(courseData),
    });

    if (!response.ok) {
      throw new Error('Failed to create course');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating course:', error);
    throw error;
  }
};

export const uploadPicToCourse = async (courseId, file) => {
  try {
    const formData = new FormData();
    formData.append('pic', file);

    const response = await axios.put(`http://localhost:8000/courses/pic/${courseId}`, formData, {
      method: 'PUT',
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${authToken}`,
      },
    });

    if (response.status === 200) {
      console.log('Picture uploaded successfully:', response.data);
    } else {
      throw new Error('Failed to upload picture');
    }
  } catch (error) {
    console.error('Error uploading picture:', error);
  }
};

export const fetchPendingApprovalsForStudents = async (teacherId) => {
  try {
    const response = await fetch(`http://localhost:8000/users/pending_approval/students/${teacherId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(error);
  }
};
  
export const handleApproveEnrollment = async(studentId, courseId) => {
  const authorization = `Bearer ${authToken}`; 

    try {
      const response = await fetch(`http://localhost:8000/users/${studentId}/teacher_approval/${courseId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: authorization
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to approve enrollment');
      }
    } catch (error) {
      throw new Error(error.message);
    }
};

export const fetchReportByCourseId = async(courseId) => {
  

  try {
    const response = await fetch(`http://localhost:8000/courses/${courseId}/reports`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    // Handle successful response
    const data = await response.json();
    return data;
  } catch (error) {
    // Handle fetch error
    console.error('Error fetching reports:', error);
    throw error;
  }
}















