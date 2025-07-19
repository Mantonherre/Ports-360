import MapView from './components/MapView'
import SensorTable from './components/SensorTable'
import SensorControls from './components/SensorControls'
import EnergyGauge from './components/EnergyGauge'
import LoginForm from './components/LoginForm'
import { WebSocketProvider } from './utils/ws'
import { FakeDataProvider } from './utils/mock'
import { useState } from 'react'

export default function App() {
  const [token, setToken] = useState(() =>
    import.meta.env.VITE_API_TOKEN || localStorage.getItem('token') || '',
  )

  if (!token) {
    return <LoginForm onSuccess={() => setToken(localStorage.getItem('token') || '')} />
  }

  const content = (
    <div className="container mx-auto p-4 grid gap-4 grid-cols-1 md:grid-cols-2">
      <div className="h-96 md:row-span-2">
        <MapView />
      </div>
      <div className="bg-white p-4 rounded shadow">
        <EnergyGauge />
      </div>
      <div className="bg-white p-4 rounded shadow">
        <SensorTable />
      </div>
      <div className="bg-white p-4 rounded shadow">
        <SensorControls />
      </div>
    </div>
  )

  if (import.meta.env.VITE_WS_ENDPOINT !== undefined) {
    return <WebSocketProvider>{content}</WebSocketProvider>
  }
  return <FakeDataProvider auto={false}>{content}</FakeDataProvider>
}
