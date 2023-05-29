

export const handleUnsubscribeFromCourse = async (courseId) => {
    const authToken = localStorage.getItem('authToken');
    const user_id = 57
    
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
  const authToken = localStorage.getItem('authToken');

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
