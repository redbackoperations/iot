import * as React from 'react'
import { Link } from 'react-router-dom'
import TableContainer from '@mui/material/TableContainer'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Box from '@mui/material/Box'
import Skeleton from '@mui/material/Skeleton'
import Typography from '@mui/material/Typography'
import { jsonFields, idFields } from '../../lib/jsonHelper'
import DeviceData from '../../interfaces/device-data'

export default function RecentList({ data, loading }: { data: DeviceData[]; loading: boolean }) {
  return (
    <>
      <Typography component="p" color="secondary" variant="h6">
        Recent Device/Sensor Data
      </Typography>

      {loading ? (
        <>
          <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
          <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
          <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
          <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
          <Skeleton animation="wave" sx={{ height: '50px' }}></Skeleton>
        </>
      ) : data && data.length > 0 ? (
        <>
          <TableContainer>
            <Table size="small" sx={{ overflow: 'scroll' }}>
              <TableHead>
                <TableRow>
                  {Object.keys(data[0]).map((fieldName) => (
                    <TableCell key={fieldName}>{fieldName}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {data.map((row: any) => (
                  <TableRow key={row._id}>
                    {Object.keys(data[0]).map((fieldName) => (
                      <TableCell key={`${row._id}-${fieldName}`}>
                        {idFields.includes(fieldName) && fieldName !== '_id' ? (
                          <Link
                            to={`/${
                              fieldName === 'deviceId'
                                ? `devices/${row.deviceId}`
                                : `bikes/${row.bikeId}`
                            }/edit`}
                          >
                            {row[fieldName]}
                          </Link>
                        ) : jsonFields.includes(fieldName) ? (
                          JSON.stringify(row[fieldName])
                        ) : (
                          row[fieldName]
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Box sx={{ mt: 1 }}>
            <Link to="/device-data">see more data</Link>
          </Box>
        </>
      ) : (
        <Typography
          variant="h6"
          noWrap
          component="div"
          mt={2}
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          No device data yet!
        </Typography>
      )}
    </>
  )
}
