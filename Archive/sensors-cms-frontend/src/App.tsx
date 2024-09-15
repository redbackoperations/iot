import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Box from '@mui/material/Box'
import CssBaseline from '@mui/material/CssBaseline'
import Toolbar from '@mui/material/Toolbar'
import Dashboard from './pages/Dashboard'
import Bikes from './pages/Bikes'
import UpsertBike from './pages/UpsertBike'
import UpsertDevice from './pages/UpsertDevice'
import Devices from './pages/Devices'
import DeviceData from './pages/DeviceData'
import TopBar from './components/TopBar'
import SideBar from './components/SideBar'
import StrengthWorkoutPage from './pages/Strength'
import EnduranceWorkoutPage from './pages/Endurance'

import './App.css'

import UsersPage from './pages/Users'
import WorkoutPage from './pages/workouts'
import ThresholdWorkoutPage from './pages/Threshold'


function App() {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <CssBaseline />
      <TopBar />
      <SideBar />

      <Box
        component="main"
        sx={{
          backgroundColor: (theme) =>
            theme.palette.mode === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
          flexGrow: 1,
          height: '100vh',
          overflow: 'auto',
          p: 3,
          width: 1,
        }}
      >
        <Toolbar />
        <Toolbar sx={{ display: { xs: 'block', sm: 'none' } }} />

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="bikes" element={<Bikes />} />
          <Route path="bikes/new" element={<UpsertBike />} />
          <Route path="bikes/:id/edit" element={<UpsertBike />} />
          <Route path="devices" element={<Devices />} />
          <Route path="devices/new" element={<UpsertDevice />} />
          <Route path="devices/:id/edit" element={<UpsertDevice />} />
          <Route path="device-data" element={<DeviceData />} />
          <Route path='/workouts' element={<WorkoutPage/>} />
          <Route path='Users' element={<UsersPage/>} />
          <Route path='strength' element={<StrengthWorkoutPage/>} />
          <Route path='threshold' element={<ThresholdWorkoutPage/>} />
          <Route path='endurance' element={<EnduranceWorkoutPage/>} />
        </Routes>
      </Box>
    </Box>
  )
}
export default App
