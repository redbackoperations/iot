import React, { useState, useEffect } from 'react'
import Grid from '@mui/material/Grid'
import DataCountCard from '../components/DataCountCard'
import DirectionsBike from '@mui/icons-material/DirectionsBike'
import DevicesIcon from '@mui/icons-material/Devices'
import DataObjectIcon from '@mui/icons-material/DataObject'
import { lightBlue, teal, orange, cyan } from '@mui/material/colors'
import moment from 'moment'
import LineChart from '../components/DeviceData/LineChart'
import PieChart from '../components/DeviceData/PieChart'
import RecentList from '../components/DeviceData/RecentList'
import AlertPopup from '../components/AlertPopup'
import { TotalCount, DeviceDataCount } from '../interfaces/data-analytics'
import DeviceData from '../interfaces/device-data'
import axiosClient from '../lib/axiosClient'
import { generateChartData, groupChartData } from '../lib/dataHelper'
import { DeviceType } from '../interfaces/device'
import mqttClient from '../lib/mqttClient'
import { isJson } from '../lib/jsonHelper'

// a counter to limit the refresh rate
let dataRefreshCounter = 0
const dataRefreshRate = process.env.REACT_APP_FETCH_DATA_RATE || 30

function Dashboard() {
  const [axiosError, setAxiosError] = useState<string | null>(null)
  const [mqttMessage, setMqttMessage] = useState<string | null>(null)
  const [showMqttMessage, setShowMqttMessage] = useState(false)
  const [deviceData, setDeviceData] = useState<DeviceData[]>([])
  const [totalCountData, setTotalCountData] = useState<TotalCount | null>(null)
  const [deviceDataCountData, setDeviceDataCountData] = useState<DeviceDataCount | null>(null)
  const [deviceDataloading, setDeviceDataLoading] = useState<boolean>(true)
  const [totalCountloading, setTotalCountLoading] = useState<boolean>(true)
  const [deviceDataCountloading, setDeviceDataCountloading] = useState<boolean>(true)

  const fetchData = () => {
    setDeviceDataLoading(true)
    setTotalCountLoading(true)
    setDeviceDataCountloading(true)

    axiosClient
      .get('/data-analytics/total-count')
      .then((response: any) => {
        setTotalCountLoading(false)
        setTotalCountData(response.data)
      })
      .catch((error) => {
        setTotalCountLoading(false)
        const message = `Get total count data failed: ${error.message}`
        console.error(message)
        setAxiosError(message)
      })

    axiosClient
      .get('/data-analytics/device-data/total-count')
      .then((response: any) => {
        setDeviceDataCountloading(false)
        setDeviceDataCountData(response.data)
      })
      .catch((error) => {
        setDeviceDataCountloading(false)
        const message = `Get total count for different device types failed: ${error.message}`
        console.error(message)
        setAxiosError(message)
      })

    axiosClient
      .get('/device-data/many?limit=200')
      .then((response: any) => {
        setDeviceDataLoading(false)
        setDeviceData(response.data.deviceData)
      })
      .catch((error) => {
        setDeviceDataLoading(false)
        const message = `Get device data failed: ${error.message}`
        console.error(message)
        setAxiosError(message)
      })
  }

  useEffect(() => {
    fetchData()

    console.log('connecting to MQTT ...')
    const client = mqttClient()

    client.on('connect', () => {
      console.log('Connected to the MQTT broker!')
    })

    client.on('error', (error) => {
      console.log(error)
    })

    client.on('message', (topic, message) => {
      const msg = message.toString()
      console.log(`[${topic}] Received message:`, msg)

      const jsonData = isJson(msg)
      dataRefreshCounter += 1

      if (dataRefreshCounter === dataRefreshRate) {
        dataRefreshCounter = 1

        // only re-fetching data when the payload including expected json format
        if (
          jsonData &&
          (jsonData.timestamp || jsonData.reportedAt) &&
          jsonData.hasOwnProperty('value')
        ) {
          // a valid data, force the page to refresh
          fetchData()
          setShowMqttMessage(true)
          setMqttMessage(
            `A new sensor data is reported to MQTT at "${moment
              .utc(jsonData.reportedAt)
              .format('DD/MM/YYYY hh:mm.SSS A')}", reteching data now...`
          )
        }
      }
    }
    )

    client.subscribe(process.env.REACT_APP_MQTT_TOPIC_TO_REFRESH_WEB_PAGE as string)

    return () => {
      console.log('leaving dashboard page, disconnecting from MQTT ...')
      client.end()
    }
  }, [])

  const groupedData = groupChartData(generateChartData(deviceData))

  return (
    <>
      <Grid container spacing={3} justifyContent="start" alignContent={'center'} textAlign="center">
        <Grid item xs={12} md={4} lg={4}>
          <DataCountCard
            title="Bikes"
            value={totalCountData?.bikes}
            icon={<DirectionsBike />}
            iconBgColor={lightBlue[300]}
            sxProps={{
              height: '200px',
              width: '100%',
              bgcolor: cyan[50],
              boxShadow: 'none',
            }}
            loading={totalCountloading}
             description="number of bikes"
          />
        </Grid>
        <Grid item xs={12} md={4} lg={4}>
          <DataCountCard
            title="Devices"
            value={totalCountData?.devices}
            icon={<DevicesIcon />}
            iconBgColor={teal[300]}
            sxProps={{
              height: 200,
              width: '100%',
              bgcolor: cyan['A100'],
              boxShadow: 'none',
            }}
            loading={totalCountloading}
             description="number of sensors/devices"
          />
        </Grid>
        <Grid item xs={12} md={4} lg={4}>
          <DataCountCard
            title="Device Data"
            value={totalCountData?.deviceData}
            icon={<DataObjectIcon />}
            iconBgColor={orange[300]}
            sxProps={{
              height: 200,
              width: '100%',
              bgcolor: cyan[100],
              boxShadow: 'none',
            }}
            loading={totalCountloading}
             description="number of sensors/devices data"
          />
        </Grid>
        <Grid item xs={12} md={3} lg={3}>
          <PieChart data={deviceDataCountData} loading={deviceDataCountloading} />
        </Grid>
        {Object.values(DeviceType).map(
          (deviceType) =>
            groupedData &&
            groupedData[deviceType] && (
              <Grid
                key={deviceType}
                item
                xs={12}
                md={3}
                lg={3}
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-evenly',
                }}
              >
                <LineChart data={groupedData[deviceType]} loading={deviceDataloading} />
              </Grid>
            )
        )}

        <Grid item xs={12} md={12} lg={12}>
          <RecentList data={deviceData} loading={deviceDataloading} />
        </Grid>
      </Grid>
      {axiosError && <AlertPopup message={axiosError} />}
      {mqttMessage && (
        <AlertPopup
          message={mqttMessage}
          showAlert={showMqttMessage}
          setShowAlert={setShowMqttMessage}
          severity="info"
        />
      )}
    </>
  )
}

export default Dashboard
