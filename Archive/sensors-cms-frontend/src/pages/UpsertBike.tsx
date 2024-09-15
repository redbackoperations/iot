import { useState, useEffect } from 'react'
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
import { useNavigate, useParams } from 'react-router-dom'
import { omit } from 'lodash'
import IBike from '../interfaces/bike'
import { ignoredDBAttributes } from '../lib/jsonHelper'

function UpsertBike() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [axiosMessage, setAxiosMessage] = useState<string | null>(null)
  const [showAlert, setShowAlert] = useState(false)
  const [severity, setSeverity] = useState('error')
  const [bikeData, setBikeData] = useState<IBike | null>(null)

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
        .get(`/bike?id=${id}`)
        .then((response: any) => {
          setBikeData(omit(response.data.bike as IBike, ignoredDBAttributes) as IBike)
        })
        .catch((error) => {
          const message = `Get bike data failed: ${error.message}`
          console.error(message)
          setAxiosMessage(message)
        })
    }
  }, [id])

  useEffect(() => {
    if (bikeData) {
      Object.entries(bikeData).forEach(([name, value]) => {
        if (name !== '_id') setValue(name, value)
      })
    }
  }, [setValue, bikeData])

  const submitForm = (data: any) => {
    console.log(data)
    axiosClient
      .request({
        method: id ? 'put' : 'post',
        url: id ? `bikes/${id}` : '/bikes',
        data: { bike: data },
      })
      .then((response: any) => {
        reset()
        console.log(response)
        setSeverity('success')
        setShowAlert(true)
        setAxiosMessage(
          id ? `Bike '${id}' data has been updated!` : 'A new bike data has been created!'
        )

        window.setTimeout(() => {
          navigate('/bikes')
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
            {id ? 'Edit Bike' : 'Create A New Bike'}
          </Typography>
          <Box
            component="form"
            sx={{
              '& .MuiTextField-root': { m: 3, width: '30ch' },
            }}
            noValidate
            autoComplete="on"
            // onSubmit={handleSubmit}
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
                label="MQTT topic prefix"
                {...register('mqttTopicPrefix', {
                  required: { value: true, message: 'cannot be blank' },
                })}
                error={!!errors.mqttTopicPrefix}
                helperText={
                  errors.mqttTopicPrefix ? (errors.mqttTopicPrefix.message as string) : ''
                }
                InputLabelProps={id ? { shrink: true } : {}}
              />
              <TextField
                required
                id="outlined-required"
                label="MQTT report topic suffix"
                {...register('mqttReportTopicSuffix', {
                  required: { value: true, message: 'cannot be blank' },
                })}
                error={!!errors.mqttReportTopicSuffix}
                helperText={
                  errors.mqttReportTopicSuffix
                    ? (errors.mqttReportTopicSuffix.message as string)
                    : ''
                }
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

export default UpsertBike
