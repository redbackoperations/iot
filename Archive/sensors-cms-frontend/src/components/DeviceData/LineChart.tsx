import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Scatter,
  ResponsiveContainer,
} from 'recharts'
import { sample } from 'lodash'
import moment from 'moment'
import { availableChartColors } from '../../lib/dataHelper'
import { ChartData } from '../../interfaces/data-analytics'
import Skeleton from '@mui/material/Skeleton'
import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'

function DeviceDataLineChart({ data, loading }: { data: ChartData[]; loading?: boolean }) {
  if (loading) {
    return (
      <div>
        <Typography
          component="div"
          key={'line-chart-loading-1'}
          variant={'h4'}
          width="100%"
          alignItems="center"
        >
          <Skeleton />
        </Typography>
        <Typography
          component="div"
          key={'line-chart-loading-2'}
          variant={'h4'}
          width="100%"
          alignItems="center"
        >
          <Skeleton />
        </Typography>
        <Typography
          component="div"
          key={'line-chart-loading-3'}
          variant={'h4'}
          width="100%"
          alignItems="center"
        >
          <Skeleton />
        </Typography>
      </div>
    )
  }

  return (
    data && (
      <Paper
        sx={{
          p: 1,
          // display: 'flex',
          // flexDirection: 'column',
          // // height: 200,
          // // width: 200,
          borderRadius: 2,
          // justifyContent: 'center',
          // alignItems: 'center',
          boxShadow:
            '0px 0 0 -1px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 10%)',
          // ...sxProps,
        }}
      >
        <ResponsiveContainer width="100%" height={400}>
          <LineChart
            data={data}
            margin={
              {
                // top: 20,
                // right: 20,
                // bottom: 20,
                // left: 20,
              }
            }
          >
            <CartesianGrid stroke="#f5f5f5" />
            <XAxis
              dataKey="reportedAt"
              axisLine={true}
              minTickGap={60}
              tick={{ fontSize: 15 }}
              scale="band"
              name={data[0].type}
              tickFormatter={(unixTime) =>
                moment(unixTime, 'DD/MM/YYYY hh:mm:ss.SSS').format('DD/MM/YYYY HH:mm')
              }
            />
            <YAxis />
            <Tooltip formatter={(value) => `${value} ${data[0].unit}`} />
            <Legend formatter={(name) => `${name} (${data[0].unit})`} />
            <Line
              type="monotone"
              dataKey="value"
              name={data[0].type}
              stroke={sample(availableChartColors)}
            />

            <Scatter dataKey="cnt" fill="red" />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    )
  )
}

export default DeviceDataLineChart
