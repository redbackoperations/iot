import * as React from 'react'
import Skeleton from '@mui/material/Skeleton'

function TableLoadingSkeletons() {
  return (
    <>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
      <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
    </>
  )
}

export default TableLoadingSkeletons
