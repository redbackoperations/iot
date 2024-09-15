import React from 'react';
import { Grid, Typography, Card, CardContent, Box, styled } from '@mui/material';
import { Link } from 'react-router-dom';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import DirectionsRunIcon from '@mui/icons-material/DirectionsRun';

const WorkoutCard = styled(Card)(({ theme }) => ({
  cursor: 'pointer',
  '&:hover': {
    transform: 'scale(1.05)',
  },
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#1aeaed',
  transition: 'transform 0.2s ease-in-out',
}));

const IconContainer = styled(Box)({
  marginBottom: '16px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
});

const CenteredParagraph = styled(Typography)({
  textAlign: 'center',
  padding: '20px 0',
});

const WorkoutPage: React.FC = () => {
  const workoutCategories = [
    {
      title: 'Strength Training',
      value: 8,
      description: 'Build muscle and increase strength with this workout.',
      icon: <FitnessCenterIcon fontSize="large" />,
      link: '/strength', // Add a link property to specify the destination page
    },
    {
      title: 'Threshold Workout',
      value: 10,
      description: 'Improve your endurance and push your limits in this workout.',
      icon: <DirectionsRunIcon fontSize="large" />,
      link: '/threshold', // Add a link property for the Threshold Workout page
    },
    {
      title: 'Endurance Workout',
      value: 15,
      description: 'Enhance your stamina and cardiovascular fitness.',
      icon: <DirectionsRunIcon fontSize="large" />,
      link: '/endurance', // Add a link property for the Endurance Workout page
    },
    {
      title: 'Ramped Workout',
      value: 12,
      description: 'Gradually increase intensity for a challenging session.',
      icon: <DirectionsRunIcon fontSize="large" />,
      link: '/ramped', // Add a link property for the Ramped Workout page
    },
  ];

  return (
    <div className="workout-page">
      <Typography variant="h2" align="center" gutterBottom>
        Welcome to Workouts
      </Typography>
      <CenteredParagraph variant="body1">
        Get ready to improve your fitness with our diverse workout categories. Whether you're
        looking to build strength or enhance endurance, we have something for everyone.
      </CenteredParagraph>
      <Grid container spacing={2} justifyContent="center">
        {workoutCategories.map((category, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <Link to={category.link} className="button-link">
              <WorkoutCard>
                <CardContent>
                  <IconContainer>{category.icon}</IconContainer>
                  <Typography variant="h5" component="div" align="center">
                    {category.title}
                  </Typography>
                  <Typography variant="body2" align="center" gutterBottom>
                    {category.description}
                  </Typography>
                  <Typography variant="h4" component="div" align="center">
                    {category.value}
                  </Typography>
                </CardContent>
              </WorkoutCard>
            </Link>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default WorkoutPage;
