import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Box from '@mui/material/Box'
import CssBaseline from '@mui/material/CssBaseline'
import Toolbar from '@mui/material/Toolbar'
import Dashboard from './pages/Dashboard'
import Bikes from './pages/Bikes'
import Devices from './pages/Devices'
import DeviceData from './pages/DeviceData'
import TopBar from './components/TopBar'
import SideBar from './components/SideBar'

import './App.css'

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <TopBar />
      <SideBar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="bikes" element={<Bikes />} />
          <Route path="devices" element={<Devices />} />
          <Route path="device-data" element={<DeviceData />} />
        </Routes>
      </Box>
    </Box>
  )
}
export default App
