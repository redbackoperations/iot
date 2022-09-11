import React from 'react'
import { Link } from 'react-router-dom'
import Box from '@mui/material/Box'
import Drawer from '@mui/material/Drawer'
import Toolbar from '@mui/material/Toolbar'
import List from '@mui/material/List'
import Divider from '@mui/material/Divider'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import InboxIcon from '@mui/icons-material/MoveToInbox'
import MailIcon from '@mui/icons-material/Mail'
import Home from '@mui/icons-material/Home'
import DirectionsBike from '@mui/icons-material/DirectionsBike'
import DevicesIcon from '@mui/icons-material/Devices'
import DataObjectIcon from '@mui/icons-material/DataObject'

const drawerWidth = 240

function SideBar() {
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
        <List>
          <Link to="/">
            {' '}
            <ListItem key={'home'} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <Home />
                </ListItemIcon>
                <ListItemText primary={'Home'} />
              </ListItemButton>
            </ListItem>
          </Link>

          <Link to="/bikes">
            <ListItem key={'bike'} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <DirectionsBike />
                </ListItemIcon>
                <ListItemText primary={'Bikes'} />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/devices">
            <ListItem key={'device'} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <DevicesIcon />
                </ListItemIcon>
                <ListItemText primary={'Devices'} />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/device-data">
            <ListItem key={'device-data'} disablePadding>
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
        <List>
          {['Users', 'Workouts', 'Others'].map((text, index) => (
            <ListItem key={text} disablePadding>
              <ListItemButton>
                <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  )
}
export default SideBar
