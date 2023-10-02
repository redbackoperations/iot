import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Button,
  Table,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
} from '@mui/material';
import { styled } from '@mui/system';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';

const PageContainer = styled(Container)(({ theme }) => ({
  marginTop: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
}));

const ContentContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: '600px',
}));

const Heading = styled(Typography)({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: '1rem',
});

const Description = styled(Typography)({
  fontSize: '1.2rem',
  textAlign: 'center',
  marginBottom: '1.5rem',
});

const ActionButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const TableContainerWrapper = styled(TableContainer)(({ theme }) => ({
  marginTop: '2rem',
  '& .MuiPaper-root': {
    // This targets the Paper component inside TableContainer
    background: 'transparent', // Set the background of Paper to transparent
  },
}));

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  background: '#2196f3', // Blue background for headings
  color: 'white',
  fontWeight: 'bold',
}));

const StrengthWorkoutPage: React.FC = () => {
  return (
    <PageContainer>
      <Heading>Strength Workout</Heading>
      <ContentContainer elevation={3}>
        <Description>
          Strengthen your body and improve your fitness with our challenging strength workouts. Our workouts are designed to help you build muscle, increase endurance, and enhance your overall strength and power.
        </Description>
        <FitnessCenterIcon style={{ fontSize: '4rem', color: '#4caf50' }} />
        <ActionButton variant="contained" color="primary">
          Get Started
        </ActionButton>
      </ContentContainer>

      {/* Table with 4 columns and 4 rows */}
      <TableContainerWrapper style={{ marginTop: '2rem' }}>
        <Table>
          <TableHead>
            <TableRow>
              <StyledTableCell>Workout Name</StyledTableCell>
              <StyledTableCell>Device Type</StyledTableCell>
              <StyledTableCell>Time Exercised</StyledTableCell>
              <StyledTableCell>Date</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>Push-ups</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>30 minutes</TableCell>
              <TableCell>2023-09-15</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Squats</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>45 minutes</TableCell>
              <TableCell>2023-09-14</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Deadlifts</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>40 minutes</TableCell>
              <TableCell>2023-09-13</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Bench Press</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>35 minutes</TableCell>
              <TableCell>2023-09-12</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainerWrapper>
    </PageContainer>
  );
};

export default StrengthWorkoutPage;
