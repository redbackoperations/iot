import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { styled, Theme, CSSObject } from '@mui/material/styles'
import Box from '@mui/material/Box'
import MuiDrawer from '@mui/material/Drawer'
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
import IconButton from '@mui/material/IconButton'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'

const drawerWidth = 240

const openedMixin = (theme: Theme): CSSObject => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
})

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
})

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  paddingRight: theme.spacing(0, 5),
  ...theme.mixins.toolbar,
}))

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  })
)

function SideBar() {
  const { pathname } = useLocation()
  const [open, setOpen] = React.useState(true)

  return (
    <>
      <Drawer
        variant="permanent"
        open={open}
        sx={{
          display: { xs: 'none', sm: 'block' },
        }}
      >
        <Toolbar />

        <DrawerHeader>
          <IconButton onClick={() => setOpen(!open)}>
            {open ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />

        <Box sx={{ overflow: 'auto' }}>
          <List sx={{ p: 0 }}>
            <Link to="/" className="button-link">
              <ListItem
                key={'home'}
                disablePadding
                selected={pathname === '/'}
                className="button-link"
                sx={{ display: 'block' }}
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
    </>
  )
}
export default SideBar
