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
  background: '#ff9800', // Orange background for headings (for threshold workout)
  color: 'white',
  fontWeight: 'bold',
}));

const ThresholdWorkoutPage: React.FC = () => {
  return (
    <PageContainer>
      <Heading>Threshold Workout</Heading>
      <ContentContainer elevation={3}>
        <Description>
          Push your limits with our challenging threshold workouts. Improve your endurance and cardiovascular fitness while maintaining a high intensity throughout your workout.
        </Description>
        <FitnessCenterIcon style={{ fontSize: '4rem', color: '#f44336' }} />
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
              <TableCell>Interval Sprints</TableCell>
              <TableCell>Treadmill</TableCell>
              <TableCell>20 minutes</TableCell>
              <TableCell>2023-09-15</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Hill Climbs</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>40 minutes</TableCell>
              <TableCell>2023-09-14</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Tempo Run</TableCell>
              <TableCell>Treadmill</TableCell>
              <TableCell>30 minutes</TableCell>
              <TableCell>2023-09-13</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>High-Intensity Rowing</TableCell>
              <TableCell>Rowing Machine</TableCell>
              <TableCell>35 minutes</TableCell>
              <TableCell>2023-09-12</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainerWrapper>
    </PageContainer>
  );
};

export default ThresholdWorkoutPage;
