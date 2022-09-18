import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import Box from '@mui/material/Box'
import Drawer from '@mui/material/Drawer'
import Toolbar from '@mui/material/Toolbar'
import List from '@mui/material/List'
import Divider from '@mui/material/Divider'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter'
import HomeIcon from '@mui/icons-material/Home'
import PeopleIcon from '@mui/icons-material/People'
import DirectionsBike from '@mui/icons-material/DirectionsBike'
import DevicesIcon from '@mui/icons-material/Devices'
import DataObjectIcon from '@mui/icons-material/DataObject'

const drawerWidth = 240

function SideBar() {
  const { pathname } = useLocation()

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List sx={{ p: 0 }}>
          <Link to="/" className="button-link">
            <ListItem
              key={'home'}
              disablePadding
              selected={pathname === '/'}
              className="button-link"
            >
              <ListItemButton>
                <ListItemIcon>
                  <HomeIcon />
                </ListItemIcon>
                <ListItemText primary={'Dashboard'} />
              </ListItemButton>
            </ListItem>
          </Link>

          <Link to="/bikes" className="button-link">
            <ListItem key={'bike'} disablePadding selected={pathname === '/bikes'}>
              <ListItemButton>
                <ListItemIcon>
                  <DirectionsBike />
                </ListItemIcon>
                <ListItemText primary={'Bikes'} />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/devices" className="button-link">
            <ListItem key={'device'} disablePadding selected={pathname === '/devices'}>
              <ListItemButton>
                <ListItemIcon>
                  <DevicesIcon />
                </ListItemIcon>
                <ListItemText primary={'Devices'} />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/device-data" className="button-link">
            <ListItem key={'device-data'} disablePadding selected={pathname === '/device-data'}>
              <ListItemButton>
                <ListItemIcon>
                  <DataObjectIcon />
                </ListItemIcon>
                <ListItemText primary={'Device Data'} />
              </ListItemButton>
            </ListItem>
          </Link>
        </List>
        <Divider />
        <List sx={{ p: 0 }}>
          <ListItem key={'users'} disablePadding selected={pathname === '/users'} disabled={true}>
            <ListItemButton>
              <ListItemIcon>
                <PeopleIcon />
              </ListItemIcon>
              <ListItemText primary={'Users'} />
            </ListItemButton>
          </ListItem>
          <ListItem
            key={'workouts'}
            disablePadding
            selected={pathname === '/workouts'}
            disabled={true}
          >
            <ListItemButton>
              <ListItemIcon>
                <FitnessCenterIcon />
              </ListItemIcon>
              <ListItemText primary={'Workouts'} />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  )
}
export default SideBar
