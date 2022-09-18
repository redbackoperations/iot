import * as React from 'react'
import Typography from '@mui/material/Typography'
import { Link } from 'react-router-dom'
import Paper from '@mui/material/Paper'
import { SxProps } from '@mui/material'
import Avatar from '@mui/material/Avatar'
import Box from '@mui/material/Box'
import { lime } from '@mui/material/colors'
import { toThousands } from '../lib/dataHelper'
import Skeleton from '@mui/material/Skeleton'
import { tokebabCase } from '../lib/dataHelper'

function DataCountCard({
  sxProps,
  title,
  value,
  description,
  link,
  icon,
  iconBgColor,
  loading,
}: {
  sxProps?: SxProps
  title: string
  value?: number
  iconBgColor?: string
  description?: string
  link?: JSX.Element
  icon: JSX.Element
  loading: boolean
}) {
  return (
    <Paper
      sx={{
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        height: 200,
        width: 200,
        borderRadius: 2,
        justifyContent: 'center',
        alignItems: 'center',
        boxShadow:
          '0px 0 0 -1px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 10%)',
        ...sxProps,
      }}
    >
      {loading ? (
        <>
          <Skeleton variant="circular" key={'data-icon'} width={50} height={50}>
            <Avatar />
          </Skeleton>
          <Typography component="div" key={'data-count'} variant={'h4'} width="30%">
            <Skeleton />
          </Typography>
          <Typography component="div" key={'title'} variant={'h4'} width="30%">
            <Skeleton />
          </Typography>
        </>
      ) : (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
            {icon && (
              <Avatar sx={{ width: 50, height: 50, bgcolor: iconBgColor || lime[400] }}>
                {icon}
              </Avatar>
            )}
          </Box>
          <Typography component="p" variant="h4">
            {value ? toThousands(value) : 'N/A'}
          </Typography>
          <Typography component="h2" variant="h6" color="primary">
            <Link className="button-link" to={`/${tokebabCase(title)}`}>
              {title}
            </Link>
          </Typography>
          {description && <Typography color="text.secondary">{description}</Typography>}
          {link && <Box sx={{ mt: 2 }}>link</Box>}
        </>
      )}
    </Paper>
  )
}

export default DataCountCard
