import React, { useState, useEffect } from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import { teal } from '@mui/material/colors'
import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import { useForm } from 'react-hook-form'
import axiosClient from '../lib/axiosClient'
import AlertPopup from '../components/AlertPopup'
import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import FormControl from '@mui/material/FormControl'
import FormHelperText from '@mui/material/FormHelperText'
import Select, { SelectChangeEvent } from '@mui/material/Select'
import { useNavigate, useParams } from 'react-router-dom'
import { omit } from 'lodash'
import IDevice, { DeviceType } from '../interfaces/device'
import { jsonFields, ignoredDBAttributes } from '../lib/jsonHelper'

function UpsertDevice() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [axiosMessage, setAxiosMessage] = useState<string | null>(null)
  const [showAlert, setShowAlert] = useState(false)
  const [severity, setSeverity] = useState('error')
  const [deviceData, setDeviceData] = useState<IDevice | null>(null)
  const [selectedType, setSelectedType] = useState<DeviceType | string>('')

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm()

  useEffect(() => {
    if (id) {
      axiosClient
        .get(`/device?id=${id}`)
        .then((response: any) => {
          setDeviceData(omit(response.data.device as IDevice, ignoredDBAttributes) as IDevice)
          setSelectedType(response.data.device.deviceType)
          console.log(response.data.device)
        })
        .catch((error) => {
          const message = `Get device data failed: ${error.message}`
          console.error(message)
          setAxiosMessage(message)
        })
    }
  }, [id])

  useEffect(() => {
    if (deviceData) {
      Object.entries(deviceData).forEach(([name, value]) => {
        if (name !== '_id') setValue(name, value)
        if (jsonFields.includes(name)) setValue(name, JSON.stringify(value))
      })
    }
  }, [setValue, deviceData])

  const handleDeviceTypeChange = (event: SelectChangeEvent) => {
    setValue('deviceType', event.target.value as string)
    setSelectedType(event.target.value as string)
  }

  const submitForm = (data: any) => {
    let payload = data
    jsonFields.forEach((attribute) => {
      if (payload[attribute]) payload[attribute] = JSON.parse(payload[attribute])
    })

    console.log(payload)
    axiosClient
      .request({
        method: id ? 'put' : 'post',
        url: id ? `devices/${id}` : '/devices',
        data: { device: data },
      })
      .then((response: any) => {
        reset()
        console.log(response)
        setSeverity('success')
        setShowAlert(true)
        setAxiosMessage(
          id ? `Device '${id}' data has been updated!` : 'A new device data has been created!'
        )

        window.setTimeout(() => {
          navigate('/devices')
        }, 1500)
      })
      .catch((error) => {
        const message = error.response.data.error || error.message

        setSeverity('error')
        setShowAlert(true)
        setAxiosMessage(message)
      })
  }

  return (
    <Grid container direction="column" justifyContent="center" alignItems="center" height={'80vh'}>
      <Grid item md={6}>
        <Paper variant="outlined">
          <Typography variant="h6" noWrap component="div" mx={3} mb={0} mt={2}>
            {id ? 'Edit Device' : 'Create A New Device'}
          </Typography>
          <Box
            component="form"
            sx={{
              '& .MuiTextField-root': { m: 3, width: '30ch' },
            }}
            noValidate
            autoComplete="on"
            onSubmit={handleSubmit((data) => submitForm(data))}
          >
            <div>
              <TextField
                required
                id="outlined-required"
                label="name"
                {...register('name', { required: { value: true, message: 'cannot be blank' } })}
                error={!!errors.name}
                helperText={errors.name ? (errors.name.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <TextField
                required
                id="outlined-required"
                label="bike id"
                {...register('bikeId', {
                  required: { value: true, message: 'cannot be blank' },
                })}
                error={!!errors.bikeId}
                helperText={errors.bikeId ? (errors.bikeId.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <FormControl required sx={{ m: 3, minWidth: 120 }} error={!!errors.deviceType}>
                <InputLabel id="demo-simple-select-required-label">device type</InputLabel>
                <Select
                  labelId="demo-simple-select-required-label"
                  id="demo-simple-select-required"
                  label="device type *"
                  {...register('deviceType', {
                    required: { value: true, message: 'cannot be blank' },
                  })}
                  error={!!errors.deviceType}
                  value={selectedType}
                  onChange={handleDeviceTypeChange}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  {Object.values(DeviceType).map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </Select>
                <FormHelperText>
                  {errors.deviceType ? (errors.deviceType.message as string) : ''}
                </FormHelperText>
              </FormControl>
              <TextField
                required
                id="outlined-required"
                label="unit name"
                {...register('unitName', {
                  required: { value: true, message: 'cannot be blank' },
                })}
                error={!!errors.unitName}
                helperText={errors.unitName ? (errors.unitName.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
            </div>
            <div>
              <TextField
                required
                id="outlined-required"
                label="MQTT topic device name"
                {...register('mqttTopicDeviceName', {
                  required: { value: true, message: 'cannot be blank' },
                })}
                error={!!errors.mqttTopicPrefix}
                helperText={
                  errors.mqttTopicPrefix ? (errors.mqttTopicPrefix.message as string) : ''
                }
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <TextField
                id="outlined-required"
                label="bluetooth name"
                {...register('bluetoothName')}
                error={!!errors.bluetoothName}
                helperText={errors.bluetoothName ? (errors.bluetoothName.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <TextField
                id="outlined-required"
                label="mac address"
                {...register('macAddress')}
                error={!!errors.macAddress}
                helperText={errors.macAddress ? (errors.macAddress.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
            </div>
            <div>
              <TextField
                id="outlined-required"
                label="label"
                {...register('label')}
                error={!!errors.label}
                helperText={errors.label ? (errors.label.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <TextField
                id="outlined-multiline-flexible"
                label="description"
                multiline
                maxRows={4}
                {...register('description')}
                error={!!errors.description}
                helperText={errors.description ? (errors.description.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
            </div>
            <div>
              {/* TODO: add json editor here */}
              <TextField
                id="outlined-multiline-flexible"
                label="metadata"
                multiline
                maxRows={4}
                {...register('metadata')}
                error={!!errors.metadata}
                helperText={errors.metadata ? (errors.metadata.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
              {/* TODO: add json editor here */}
              <TextField
                id="outlined-required"
                label="bluetooth uuids"
                multiline
                maxRows={50}
                {...register('bluetoothUUIDs')}
                error={!!errors.bluetoothUUIDs}
                helperText={errors.bluetoothUUIDs ? (errors.bluetoothUUIDs.message as string) : ''}
                InputLabelProps={id ? { shrink: true } : {}}
              />
            </div>
            <Box mb={1} display="flex" justifyContent="flex-end" alignItems="flex-end">
              <Button
                type="submit"
                variant="contained"
                sx={{ m: 3, mb: 2, background: teal['A700'] }}
              >
                {id ? 'Update' : 'Create'}
              </Button>
            </Box>
            {axiosMessage && (
              <AlertPopup
                message={axiosMessage}
                showAlert={showAlert}
                setShowAlert={setShowAlert}
                severity={severity}
              />
            )}
          </Box>
        </Paper>
      </Grid>
    </Grid>
  )
}

export default UpsertDevice
