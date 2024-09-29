const API_URL = 'https://jsonplaceholder.typicode.com'; // Using JSONPlaceholder for testing

const loginService = async (email, password) => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to login');
    }

    const data = await response.json();
    return data[0]; // Returning the first user for testing
  } catch (error) {
    console.error('Login Service Error:', error);
    throw error;
  }
};

const signupService = async (email, username, password) => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, username, password }),
    });

    if (!response.ok) {
      throw new Error('Failed to sign up');
    }

    const data = await response.json();
    return data; // Returning the created user
  } catch (error) {
    console.error('Signup Service Error:', error);
    throw error;
  }
};

const getUserService = async () => {
  try {
    const response = await fetch(`${API_URL}/users/1`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch user');
    }

    const data = await response.json();
    return data; // Returning the first user
  } catch (error) {
    console.error('Get User Service Error:', error);
    throw error;
  }
};

const logoutService = async () => {
  try {
    // Clear user data from local storage or perform necessary logout operations
    localStorage.removeItem('token'); // Example operation
    return true;
  } catch (error) {
    console.error('Logout Service Error:', error);
    throw error;
  }
};

export { loginService, signupService, getUserService, logoutService };
