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
  background: '#ff5722', // Red background for headings (for endurance workout)
  color: 'white',
  fontWeight: 'bold',
}));

const EnduranceWorkoutPage: React.FC = () => {
  return (
    <PageContainer>
      <Heading>Endurance Workout</Heading>
      <ContentContainer elevation={3}>
        <Description>
          Improve your cardiovascular fitness and stamina with our endurance workouts. These workouts are designed to help you maintain a steady effort over an extended period, boosting your overall endurance.
        </Description>
        <FitnessCenterIcon style={{ fontSize: '4rem', color: '#e91e63' }} />
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
              <TableCell>Long-Distance Run</TableCell>
              <TableCell>Treadmill</TableCell>
              <TableCell>60 minutes</TableCell>
              <TableCell>2023-09-15</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Cycling Marathon</TableCell>
              <TableCell>Bike</TableCell>
              <TableCell>90 minutes</TableCell>
              <TableCell>2023-09-14</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Swim Endurance</TableCell>
              <TableCell>Swimming Pool</TableCell>
              <TableCell>45 minutes</TableCell>
              <TableCell>2023-09-13</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Hiking Expedition</TableCell>
              <TableCell>Hiking</TableCell>
              <TableCell>120 minutes</TableCell>
              <TableCell>2023-09-12</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainerWrapper>
    </PageContainer>
  );
};

export default EnduranceWorkoutPage;
