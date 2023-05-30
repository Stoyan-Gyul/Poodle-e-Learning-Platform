

const authToken = localStorage.getItem('authToken');
const user_id = 57
const role = 'teacher'

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
      console.log('Error unsubscribing from course:', error);
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
    const response = await fetch(`http://localhost:8000/courses/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
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





