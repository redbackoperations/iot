import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  useTheme,
  styled, // Import styled
} from '@mui/material';

// Import your company logo image
import logo from '../redback-logo.png';

interface User {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  password: string;
}

const FormContainer = styled(Container)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  position: 'relative', // Added to create a relative positioning context
}));

const ModalOverlay = styled(Box)(({ theme }) => ({
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent black background
  zIndex: 999, // Place it above other content
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const Form = styled('form')(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
  padding: theme.spacing(2),
  maxWidth: '400px',
  boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)',
  borderRadius: '8px',
  backgroundColor: 'white',
  zIndex: 1000, // Place it above the overlay
}));

const Input = styled(TextField)(({ theme }) => ({
  marginBottom: theme.spacing(2),
}));

const ActionButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  backgroundColor: 'black', // Set the background color to black
  color: 'white', // Set text color to white
  '&:hover': {
    backgroundColor: 'darkorange', // Set hover background color to dark orange
  },
}));

const ButtonsContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center', // Center the buttons horizontally
  gap: theme.spacing(2), // Add spacing between buttons
}));

const LoginButton = styled(Button)(({ theme }) => ({
  backgroundColor: 'black',
  color: 'white',
  '&:hover': {
    backgroundColor: 'darkorange',
  },
}));

const RegisterButton = styled(Button)(({ theme }) => ({
  backgroundColor: 'black',
  color: 'white',
  '&:hover': {
    backgroundColor: 'darkorange',
  },
}));

const UsersPage: React.FC = () => {
  const [registerUser, setRegisterUser] = useState<User>({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
  });
  const [isLoginForm, setIsLoginForm] = useState(true);
  const [showForm, setShowForm] = useState(false); // Added to control form visibility

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setRegisterUser({ ...registerUser, [name]: value });
  };

  const handleRegister = () => {
    alert(`Register - 
      First Name: ${registerUser.firstName}
      Last Name: ${registerUser.lastName}
      Username: ${registerUser.username}
      Email: ${registerUser.email}
      Password: ${registerUser.password}`);
  };

  const theme = useTheme();

  const toggleForm = (isLoginForm: boolean) => {
    setIsLoginForm(isLoginForm);
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
  };

  return (
    <FormContainer>
      {/* Display the company logo */}
      <img src={logo} alt="Redback Logo" style={{ width: '100px', marginBottom: '20px' }} />

      <ButtonsContainer>
        <LoginButton
          variant="contained"
          color="primary"
          onClick={() => toggleForm(true)}
        >
          Login
        </LoginButton>
        <RegisterButton
          variant="contained"
          color="primary"
          onClick={() => toggleForm(false)}
        >
          Register
        </RegisterButton>
      </ButtonsContainer>

      {/* Display the form within the modal overlay */}
      {showForm && (
        <ModalOverlay>
          <Form>
            <Typography variant="h5">{isLoginForm ? 'Login' : 'Register'}</Typography>
            {!isLoginForm && (
              <>
                <Input
                  label="First Name"
                  variant="outlined"
                  name="firstName"
                  value={registerUser.firstName}
                  onChange={handleInputChange}
                />
                <Input
                  label="Last Name"
                  variant="outlined"
                  name="lastName"
                  value={registerUser.lastName}
                  onChange={handleInputChange}
                />
                <Input
                  label="Email"
                  variant="outlined"
                  type="email"
                  name="email"
                  value={registerUser.email}
                  onChange={handleInputChange}
                />
              </>
            )}
            <Input
              label="Username"
              variant="outlined"
              name="username"
              value={registerUser.username}
              onChange={handleInputChange}
            />
            <Input
              label="Password"
              variant="outlined"
              type="password"
              name="password"
              value={registerUser.password}
              onChange={handleInputChange}
            />
            <ActionButton
              variant="contained"
              color="primary"
              onClick={handleRegister}
            >
              {isLoginForm ? 'Login' : 'Register'}
            </ActionButton>
            <Button variant="text" color="primary" onClick={closeForm}>
              Close
            </Button>
          </Form>
        </ModalOverlay>
      )}
    </FormContainer>
  );
};

export default UsersPage;
