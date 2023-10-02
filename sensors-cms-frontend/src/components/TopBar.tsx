import React from 'react'
import { Link } from 'react-router-dom'
import Grid from '@mui/material/Grid'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import MenuIcon from '@mui/icons-material/Menu'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import HomeIcon from '@mui/icons-material/Home'
import DirectionsBike from '@mui/icons-material/DirectionsBike'
import DevicesIcon from '@mui/icons-material/Devices'
import DataObjectIcon from '@mui/icons-material/DataObject'

import logo from '../redback-logo.png'

function TopBar() {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Grid container justifyContent="space-between" alignItems="center">
          <Grid
            item
            xs={12}
            md={10}
            justifyContent="flex-start"
            display="flex"
            // flexDirection="column"
            sx={{ mt: { xs: 1, sm: 0 } }}
          >
            <Menu
              id="mobile-menu"
              MenuListProps={{
                'aria-labelledby': 'mobile-menu-button',
              }}
              anchorEl={anchorEl}
              open={open}
              onClose={handleClose}
              PaperProps={{
                style: {
                  marginTop: 5,
                  // maxHeight: ITEM_HEIGHT * 4.5,
                  width: '100%',
                  left: 0,
                  right: 0,
                },
              }}
              elevation={1}
            >
              <Link to="/" className="button-link" onClick={handleClose}>
                <MenuItem key={'home'} className="button-link">
                  <ListItemButton sx={{ p: 0 }}>
                    <ListItemIcon>
                      <HomeIcon />
                    </ListItemIcon>
                    <ListItemText primary={'Dashboard'} />
                  </ListItemButton>
                </MenuItem>
              </Link>
              <Link to="/bikes" className="button-link" onClick={handleClose}>
                <MenuItem key={'bike'}>
                  <ListItemButton sx={{ p: 0 }}>
                    <ListItemIcon>
                      <DirectionsBike />
                    </ListItemIcon>
                    <ListItemText primary={'Bikes'} />
                  </ListItemButton>
                </MenuItem>
              </Link>
              <Link to="/devices" className="button-link" onClick={handleClose}>
                <MenuItem key={'device'}>
                  <ListItemButton sx={{ p: 0 }}>
                    <ListItemIcon>
                      <DevicesIcon />
                    </ListItemIcon>
                    <ListItemText primary={'Devices'} />
                  </ListItemButton>
                </MenuItem>
              </Link>
              <Link to="workouts" className="button-link" onClick={handleClose}>
                <MenuItem key={'workouts'}>
                  <ListItemButton sx={{ p: 0 }}>
                    <ListItemIcon>
                      <DataObjectIcon />
                    </ListItemIcon>
                    <ListItemText primary={'Workouts'} />
                  </ListItemButton>
                </MenuItem>
              </Link>

              <Link to="/device-data" className="button-link" onClick={handleClose}>
                <MenuItem key={'device-data'}>
                  <ListItemButton sx={{ p: 0 }}>
                    <ListItemIcon>
                      <DataObjectIcon />
                    </ListItemIcon>
                    <ListItemText primary={'Device Data'} />
                  </ListItemButton>
                </MenuItem>
              </Link>

            </Menu>
            <Typography variant="h6" noWrap component="div">
              Redback Operations / IoT CMS
            </Typography>
          </Grid>
          <Grid
            item
            xs={12}
            md={2}
            sx={{
              display: 'flex',
              // alignContent: '',
              justifyContent: { xs: 'space-between', sm: 'flex-end' },
              mb: 0.5,
            }}
          >
            <IconButton
              id="mobile-menu-button"
              color="inherit"
              edge="start"
              // onClick={() => handleDrawerOpen(!open)}
              sx={{ display: { xs: 'block', sm: 'none' }, mb: 0, pb: 0 }}
              aria-label="more"
              aria-controls={open ? 'mobile-menu' : undefined}
              aria-expanded={open ? 'true' : undefined}
              aria-haspopup="true"
              onClick={handleClick}
            >
              <MenuIcon />
            </IconButton>
            <img src={logo} alt="redback-logo" width={60} />
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  )
}
export default TopBar
