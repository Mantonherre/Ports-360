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
}

export const useStore = create<State>(() => ({
  bathyPoints: [],
  sensorReadings: [],
  stateOfCharge: 0,
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

export function FakeDataProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
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
  }, [])
  return <>{children}</>
}
