import React from 'react'

import Grid from '@mui/material/Grid'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'

import logo from '../redback-logo.png'

function TopBar() {
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Grid container justifyContent="space-between" alignItems="center">
          <Grid item md={11}>
            <Typography variant="h6" noWrap component="div">
              Redback Operations / Sensors Data CMS
            </Typography>
          </Grid>
          <Grid item md={1} sx={{ display: 'contents' }}>
            <img src={logo} alt="redback-logo" width={60} />
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  )
}
export default TopBar
