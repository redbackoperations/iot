import React from 'react'
import {
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
  ResponsiveContainer,
  PieLabelRenderProps,
} from 'recharts'
import { grey } from '@mui/material/colors'
import CircularProgress from '@mui/material/CircularProgress'
import Paper from '@mui/material/Paper'
import { DeviceDataCount } from '../../interfaces/data-analytics'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

const RADIAN = Math.PI / 180
const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
  index,
}: PieLabelRenderProps) => {
  const radius = Number(innerRadius) + (Number(outerRadius) - Number(innerRadius)) * 0.65
  const x = Number(cx) + radius * Math.cos(-midAngle * RADIAN)
  const y = Number(cy) + radius * Math.sin(-midAngle * RADIAN)

  return (
    <text x={x} y={y} fill={grey[900]} textAnchor="middle" dominantBaseline="central">
      {`${(percent! * 100).toFixed(0)}%`}
    </text>
  )
}

function DeviceDataPieChart({
  data,
  loading,
}: {
  data: DeviceDataCount | null
  loading?: boolean
}) {
  const chartData = data
    ? Object.keys(data)
        .filter((deviceType: string) => deviceType !== 'total')
        .map((deviceType: string) => ({
          name: deviceType,
          value: data[deviceType],
        }))
    : []

  return loading ? (
    <CircularProgress style={{ width: '300px', height: '300px' }} color="info" />
  ) : (
    <Paper
      sx={{
        p: 1,
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        borderRadius: 2,
        justifyContent: 'center',
        boxShadow:
          '0px 0 0 -1px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 5%), 0px 1px 1px 0px rgb(0 0 0 / 10%)',
      }}
    >
      <ResponsiveContainer width="100%" height={360}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={150}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  )
}

export default DeviceDataPieChart
