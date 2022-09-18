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
    )
  )
}

export default DeviceDataLineChart
