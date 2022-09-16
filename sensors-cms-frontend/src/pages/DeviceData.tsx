import { useState, useEffect } from 'react'
import { styled } from '@mui/material/styles'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell, { tableCellClasses } from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'
import axiosClient from '../lib/axiosClient'
import { jsonFields } from '../lib/jsonHelper'
import AlertPopup from '../components/AlertPopup'

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.primary.light,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 12,
  },
}))

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}))

function DeviceData() {
  const [axiosError, setAxiosError] = useState<string | null>(null)
  const [deviceData, setDeviceData] = useState<any | null>(null)

  useEffect(() => {
    axiosClient
      .get('/device-data/many')
      .then((response: any) => {
        console.log(response)
        setDeviceData(response.data.deviceDatas)
      })
      .catch((error) => {
        const message = `Get device data failed: ${error.message}`
        console.error(message)
        setAxiosError(message)
      })
  }, [])

  return (
    <>
      {deviceData ? (
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 500 }} aria-label="device-data-table">
            <TableHead>
              <TableRow>
                {Object.keys(deviceData[0]).map((fieldName) => (
                  <StyledTableCell key={fieldName}>{fieldName}</StyledTableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {deviceData.map((row: any) => (
                <StyledTableRow key={row._id}>
                  {Object.keys(deviceData[0]).map((fieldName) => (
                    <StyledTableCell key={`${row._id}-${fieldName}`}>
                      {jsonFields.includes(fieldName)
                        ? JSON.stringify(row[fieldName])
                        : row[fieldName]}
                    </StyledTableCell>
                  ))}
                </StyledTableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <h5>Loading data ...</h5>
      )}
      {axiosError && <AlertPopup message={axiosError} />}
    </>
  )
}

export default DeviceData
