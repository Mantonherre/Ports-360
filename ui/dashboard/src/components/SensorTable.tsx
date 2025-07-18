import { useStore } from '../utils/mock'

export default function SensorTable() {
  const sensors = useStore(s => s.sensorReadings)

  return (
    <div>
      <h2 className="font-bold mb-2">Latest Sensors</h2>
      <table className="table-auto w-full text-sm">
        <thead>
          <tr>
            <th>ID</th>
            <th>Property</th>
            <th>Value</th>
            <th>Unit</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {sensors.slice(0, 10).map(r => (
            <tr key={r.id + r.timestamp} className="odd:bg-gray-100">
              <td>{r.id}</td>
              <td>{r.property}</td>
              <td>{r.value}</td>
              <td>{r.unit}</td>
              <td>{new Date(r.timestamp).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
