import MapView from './components/MapView'
import SensorTable from './components/SensorTable'
import EnergyGauge from './components/EnergyGauge'
import { WebSocketProvider } from './utils/ws'

export default function App() {
  return (
    <WebSocketProvider>
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
      </div>
    </WebSocketProvider>
  )
}
