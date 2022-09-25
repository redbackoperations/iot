import * as React from 'react'
import { Link } from 'react-router-dom'
import TableContainer from '@mui/material/TableContainer'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Box from '@mui/material/Box'
import Alert from '@mui/material/Alert'
import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'
import { jsonFields, idFields } from '../../lib/jsonHelper'
import DeviceData from '../../interfaces/device-data'
import TableLoadingSkeletons from '../TableLoadingSkeletons'

export default function RecentList({ data, loading }: { data: DeviceData[]; loading: boolean }) {
  return (
    <>
      <Typography component="p" color="secondary" variant="h6">
        Recent Device/Sensor Data
      </Typography>

      {loading ? (
        <TableLoadingSkeletons />
      ) : data && data.length > 0 ? (
        <>
          <TableContainer component={Paper}>
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
          noWrap
          component="div"
          mt={5}
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <Alert severity="warning" variant="filled" sx={{ fontSize: 20 }}>
            Device/sensor data not found!
          </Alert>
        </Typography>
      )}
    </>
  )
}
