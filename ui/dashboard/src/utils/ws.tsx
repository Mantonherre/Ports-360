import { create } from 'zustand'
import { io } from 'socket.io-client'
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

export function WebSocketProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const host = window.location.host
    const base = import.meta.env.VITE_WS_ENDPOINT || `${proto}://${host}`
    const socket = io(`${base}/ws`)
    socket.on('entity_update', (data: any) => {
      if (data.type === 'BathyPoint') {
        useStore.setState(state => ({ bathyPoints: [...state.bathyPoints, data] }))
      } else if (data.type === 'SensorReading') {
        useStore.setState(state => {
          const readings = [data, ...state.sensorReadings]
          return { sensorReadings: readings.slice(0, 10) }
        })
      } else if (data.type === 'EnergyAsset') {
        useStore.setState({ stateOfCharge: data.state_of_charge })
      }
    })
    return () => {
      socket.close()
    }
  }, [])
  return <>{children}</>
}
