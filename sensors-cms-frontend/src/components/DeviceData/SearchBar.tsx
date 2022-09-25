import * as React from 'react'
import Chip from '@mui/material/Chip'
import TextField from '@mui/material/TextField'
import Autocomplete from '@mui/material/Autocomplete'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Slider from '@mui/material/Slider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Switch from '@mui/material/Switch'
import Paper from '@mui/material/Paper'
import moment from 'moment'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'
import Fab from '@mui/material/Fab'
import SearchIcon from '@mui/icons-material/Search'
import RestartAltIcon from '@mui/icons-material/RestartAlt'
import Select, { SelectChangeEvent } from '@mui/material/Select'
import FormControl from '@mui/material/FormControl'
import MenuItem from '@mui/material/MenuItem'
import InputLabel from '@mui/material/InputLabel'
import {
  FieldValues,
  useForm,
  UseFormRegister,
  UseFormSetValue,
  Controller,
  Control,
} from 'react-hook-form'
import { DeviceType } from '../../interfaces/device'

const limitValues = [
  {
    value: 10,
    label: '10',
  },
  {
    value: 20,
    label: '20',
  },
  {
    value: 50,
    label: '50',
  },
  {
    value: 100,
    label: '100',
  },
  {
    value: 500,
    label: '500',
  },
]

const defaultFormData: Record<string, any> = {
  after: null,
  before: moment.utc(),
  deviceTypes: [],
  keyword: null,
  limit: '100',
  testing: false,
  valueRange: [-10, 500],
}

const defaultValuesByField = (fieldName: string, queryData?: Record<string, any>) =>
  (queryData && queryData[fieldName]) || defaultFormData[fieldName]

function LimitSelect({
  register,
  setValue,
  loading,
  queryData,
}: {
  register: UseFormRegister<FieldValues>
  setValue: UseFormSetValue<FieldValues>
  loading?: boolean
  queryData?: Record<string, any>
}) {
  const [limit, setLimit] = React.useState(defaultValuesByField('limit', queryData))

  const handleChange = (event: SelectChangeEvent) => {
    setLimit(event.target.value as string)
    setValue('limit', event.target.value as string)
  }

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl fullWidth>
        <InputLabel id="limit-select-label">limit</InputLabel>
        <Select
          labelId="limit-select-label"
          id="limit-select"
          value={limit}
          label="limit"
          {...register('limit')}
          onChange={handleChange}
          disabled={loading}
        >
          {limitValues.map((limitValue) => (
            <MenuItem key={limitValue.label} value={limitValue.value}>
              {limitValue.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  )
}

function SearchButtons({ loading, reset }: { loading?: boolean; reset: () => void }) {
  return (
    <>
      <Fab
        type="submit"
        variant="extended"
        color="info"
        aria-label="search"
        sx={{ mr: 2 }}
        disabled={loading}
      >
        <SearchIcon sx={{ mr: 1 }} />
        Search
      </Fab>
      <Fab variant="extended" color="warning" aria-label="reset" disabled={loading} onClick={reset}>
        <RestartAltIcon sx={{ mr: 1 }} />
        Reset
      </Fab>
    </>
  )
}

const sliderMarks = [
  {
    value: -10,
    label: '-10',
  },
  {
    value: 100,
    label: '100',
  },
  {
    value: 500,
    label: '500',
  },
  {
    value: 1000,
    label: '1000',
  },
]

const minDistance = 10

function ValueRangeSlider({
  control,
  loading,
  queryData,
}: {
  control: Control<FieldValues>
  loading?: boolean
  queryData?: Record<string, any>
}) {
  const [valueRange, setValueRange] = React.useState<number[]>(
    defaultValuesByField('valueRange[]', queryData) || defaultValuesByField('valueRange', queryData)
  )

  const handleChange = (
    event: Event,
    newValue: number | number[],
    activeThumb: number,
    formOnChange: (value: Number[]) => void
  ) => {
    if (!Array.isArray(newValue)) {
      return
    }

    if (activeThumb === 0) {
      const newRange = [Math.min(newValue[0], valueRange[1] - minDistance), valueRange[1]]
      setValueRange(newRange)
      formOnChange(newRange)
    } else {
      const newRange = [valueRange[0], Math.max(newValue[1], valueRange[0] + minDistance)]
      setValueRange(newRange)
      formOnChange(newRange)
    }
  }

  return (
    <Box>
      <Typography id="value-slider-label" variant="body2">
        value
      </Typography>

      <Controller
        name="valueRange"
        control={control}
        // defaultValue={[-10, 500]}
        render={(props) => (
          <Slider
            // defaultValue={[0, 200]}
            id="value-slider"
            sx={{ m: 0, pb: 0 }}
            getAriaLabel={() => 'Minimum distance'}
            value={valueRange}
            min={-10}
            max={1000}
            onChange={(event, value, activeThumb) =>
              handleChange(event, value, activeThumb, props.field.onChange)
            }
            marks={sliderMarks}
            valueLabelDisplay="auto"
            step={minDistance}
            disabled={loading}
          />
        )}
      />
    </Box>
  )
}

function DeviceTypeSelect({
  control,
  loading,
  queryData,
}: {
  control: Control<FieldValues>
  loading?: boolean
  queryData?: Record<string, any>
}) {
  const [values, setValues] = React.useState<string[]>(
    defaultValuesByField('deviceTypes', queryData) || []
  )

  return (
    <Controller
      name="deviceTypes"
      control={control}
      render={(props) => (
        <Autocomplete
          multiple
          id="device-type-multiselect"
          value={Array.isArray(values) ? values : [values]}
          options={Object.values(DeviceType)}
          getOptionLabel={(option) => option}
          renderTags={(tagValue, getTagProps) =>
            tagValue.map((option, index) => <Chip label={option} {...getTagProps({ index })} />)
          }
          onChange={(event, newValues) => {
            setValues(newValues)
            props.field.onChange(newValues)
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              fullWidth
              label="device type"
              placeholder="please select type(s) that you want to filter with"
              variant="outlined"
              color="info"
              InputLabelProps={{ shrink: true }}
              disabled={loading}
            />
          )}
        />
      )}
    />
  )
}

function ReportTimePicker({
  name,
  label,
  defaultTime,
  control,
  loading,
  queryData,
}: {
  name: string
  label: string
  defaultTime?: moment.Moment | null
  loading?: boolean
  queryData?: Record<string, any>
  control: Control<FieldValues>
}) {
  const [value, setValue] = React.useState<moment.Moment | undefined | null>(
    // defaultTime !== undefined ? defaultTime : moment.utc()
    defaultValuesByField(name, queryData)
  )

  const handleChange = (
    newValue: moment.Moment | null | undefined,
    formOnChange: (value?: string) => void
  ) => {
    setValue(newValue)
    formOnChange(newValue?.toISOString())
  }

  return (
    <LocalizationProvider dateAdapter={AdapterMoment}>
      <Controller
        name={name}
        control={control}
        defaultValue={value && moment(value).toISOString()}
        render={(props) => (
          <DateTimePicker
            inputFormat="DD/MM/YYYY hh:mm A"
            label={label}
            value={value}
            onChange={(value) => handleChange(value, props.field.onChange)}
            renderInput={(params) => (
              <TextField
                {...params}
                InputLabelProps={{ shrink: true }}
                style={{ width: '100%' }}
                disabled={loading}
              />
            )}
          />
        )}
      />
    </LocalizationProvider>
  )
}

function SearchBar({
  handleSearchSubmit,
  loading,
  resultsCount,
  queryData,
}: {
  handleSearchSubmit: (data: any) => void
  loading?: boolean
  resultsCount?: number
  queryData: Record<string, any>
}) {
  const { register, handleSubmit, setValue, control } = useForm(queryData || defaultFormData)

  const submitForm = (data: any) => {
    handleSearchSubmit(data)
  }

  console.log(queryData)

  return (
    <Paper variant="outlined" sx={{ p: 5, mb: 2 }}>
      <form onSubmit={handleSubmit((data) => submitForm(data))}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4} lg={4}>
            <TextField
              size="medium"
              fullWidth
              label="device/bike/unit name"
              variant="outlined"
              color="info"
              //   onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              {...register('keyword')}
              disabled={loading}
              defaultValue={defaultValuesByField('keyword', queryData)}
            />
          </Grid>
          <Grid item xs={12} md={4} lg={4}>
            <DeviceTypeSelect control={control} loading={loading} queryData={queryData} />
          </Grid>
          <Grid item xs={12} md={4} lg={4}>
            <ValueRangeSlider control={control} loading={loading} queryData={queryData} />
          </Grid>
          <Grid item xs={12} md={3} lg={3}>
            <ReportTimePicker
              name="after"
              label="reported at (after)"
              control={control}
              loading={loading}
              queryData={queryData}
            />
          </Grid>
          <Grid item xs={12} md={3} lg={3}>
            <ReportTimePicker
              name="before"
              label="reported at (before)"
              control={control}
              loading={loading}
              queryData={queryData}
            />
          </Grid>
          <Grid item xs={12} md={3} lg={3}>
            <LimitSelect
              register={register}
              setValue={setValue}
              loading={loading}
              queryData={queryData}
            />
          </Grid>

          <Grid item xs={12} md={3} lg={3}>
            <FormControlLabel
              control={
                <Switch defaultChecked={defaultValuesByField('testing', queryData) === 'true'} />
              }
              label={<label className="testing-data-toggle-label">testing</label>}
              sx={{ mt: '5px' }}
              {...register('testing')}
              disabled={loading}
            />
          </Grid>
          <Grid
            item
            xs={12}
            md={6}
            lg={6}
            sx={{ display: 'flex', justifyContent: 'flex', alignItems: 'center' }}
          >
            <Typography variant="body1" component="p" sx={{ fontWeight: 1 }}>{`${
              resultsCount || 0
            } Results`}</Typography>
          </Grid>
          <Grid item xs={12} md={6} lg={6} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <SearchButtons
              loading={loading}
              reset={() => {
                window.location.href =
                  window.location.protocol + '//' + window.location.host + window.location.pathname
              }}
            />
          </Grid>
        </Grid>
      </form>
    </Paper>
  )
}

export default SearchBar
