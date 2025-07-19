import { create } from 'zustand'
import { useEffect } from 'react'

interface BathyPoint {
  id: string
  depth_m: number
  location: { type: 'Point'; coordinates: [number, number] }
  timestamp: string
}

interface SensorReading {
  id: string
  property: string
  value: number
  unit: string
  timestamp: string
}

interface State {
  bathyPoints: BathyPoint[]
  sensorReadings: SensorReading[]
  stateOfCharge: number
  addSensor: (id: string, value: number, property?: string, unit?: string) => void
  updateSensor: (id: string, value: number) => void
  removeSensor: (id: string) => void
}

export const useStore = create<State>((set, get) => ({
  bathyPoints: [],
  sensorReadings: [],
  stateOfCharge: 0,
  addSensor: (id, value, property = 'manual', unit = 'C') => {
    const reading = {
      id,
      property,
      value,
      unit,
      timestamp: new Date().toISOString(),
    }
    set(state => {
      const readings = [reading, ...state.sensorReadings]
      return { sensorReadings: readings.slice(0, 10) }
    })
  },
  updateSensor: (id, value) => {
    const reading = {
      id,
      property: 'manual',
      value,
      unit: 'C',
      timestamp: new Date().toISOString(),
    }
    set(state => {
      const filtered = state.sensorReadings.filter(r => r.id !== id)
      return { sensorReadings: [reading, ...filtered].slice(0, 10) }
    })
  },
  removeSensor: id => {
    set(state => ({
      sensorReadings: state.sensorReadings.filter(r => r.id !== id),
    }))
  },
}))

function randomBathyPoint(): BathyPoint {
  const id = Math.random().toString(36).slice(2)
  const depth = Math.round(Math.random() * 30)
  const baseLat = 38.345
  const baseLon = -0.481
  const offset = () => (Math.random() - 0.5) / 100
  return {
    id,
    depth_m: depth,
    location: { type: 'Point', coordinates: [baseLon + offset(), baseLat + offset()] },
    timestamp: new Date().toISOString(),
  }
}

function randomSensorReading(): SensorReading {
  const id = 'sensor-' + Math.floor(Math.random() * 3 + 1)
  const property = 'temperature'
  const value = Math.round(200 + Math.random() * 50) / 10
  return {
    id,
    property,
    value,
    unit: 'C',
    timestamp: new Date().toISOString(),
  }
}

function randomSoc(): number {
  return Math.round(Math.random() * 100)
}

export function FakeDataProvider({
  children,
  auto = true,
}: {
  children: React.ReactNode
  auto?: boolean
}) {
  useEffect(() => {
    if (!auto) return
    const bathy = setInterval(() => {
      const point = randomBathyPoint()
      useStore.setState(state => ({ bathyPoints: [...state.bathyPoints, point] }))
    }, 1000)

    const sensor = setInterval(() => {
      const reading = randomSensorReading()
      useStore.setState(state => {
        const readings = [reading, ...state.sensorReadings]
        return { sensorReadings: readings.slice(0, 10) }
      })
    }, 2000)

    const soc = setInterval(() => {
      useStore.setState({ stateOfCharge: randomSoc() })
    }, 5000)

    return () => {
      clearInterval(bathy)
      clearInterval(sensor)
      clearInterval(soc)
    }
  }, [auto])
  return <>{children}</>
}
