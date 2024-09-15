import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { styled } from '@mui/material/styles'
import { omitBy } from 'lodash'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell, { tableCellClasses } from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'
import { Typography } from '@mui/material'
import Alert from '@mui/material/Alert'
import qs from 'qs'
import axiosClient from '../lib/axiosClient'
import { jsonFields, idFields } from '../lib/jsonHelper'
import AlertPopup from '../components/AlertPopup'
import SearchBar from '../components/DeviceData/SearchBar'
import TableLoadingSkeletons from '../components/TableLoadingSkeletons'
import IDeviceData from '../interfaces/device-data'

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
  const [deviceData, setDeviceData] = useState<(IDeviceData[] & { total: number }) | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const navigate = useNavigate()
  const location = useLocation()

  const handleSearchSubmit = (data: object) => {
    navigate({
      pathname: '/device-data',
      search: qs.stringify(
        omitBy(data, (v) => v === null || v === undefined),
        { arrayFormat: 'brackets', encodeValuesOnly: true }
      ),
    })
    setLoading(true)

    axiosClient
      .get('/device-data/many', { params: data })
      .then((response: any) => {
        setLoading(false)
        setDeviceData(response.data.deviceData)
      })
      .catch((error: Error) => {
        setLoading(false)
        const message = `Get device data failed: ${error.message}`
        console.error(message)
        setAxiosError(message)
      })
  }

  useEffect(() => {
    if (!deviceData) {
      axiosClient
        .get(`/device-data/many${location.search?.length > 1 ? location.search : '?limit=100'}`)
        .then((response: any) => {
          setLoading(false)
          setDeviceData(response.data.deviceData)
        })
        .catch((error) => {
          setLoading(false)
          const message = `Get device data failed: ${error.message}`
          console.error(message)
          setAxiosError(message)
        })
    }
  }, [deviceData, location.search])

  return (
    <>
      <SearchBar
        handleSearchSubmit={handleSearchSubmit}
        loading={loading}
        resultsCount={deviceData?.length}
        queryData={qs.parse(location.search, { ignoreQueryPrefix: true })}
      />
      /*
      {loading ? ( 
        <TableLoadingSkeletons />
      ) : deviceData && deviceData.length > 0 ? (
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
                    </StyledTableCell>
                  ))}
                </StyledTableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Typography
          noWrap
          component="div"
          mt={40}
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <Alert severity="warning" variant="filled" sx={{ fontSize: 20 }}>
            Device data not found!
          </Alert>
        </Typography>
      )}

      {axiosError && <AlertPopup message={axiosError} />}
    </>
  )
}

export default DeviceData
