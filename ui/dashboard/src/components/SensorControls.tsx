import { useStore } from '../utils/mock'
import { patchEntity } from '../utils/api'

export default function SensorControls() {
  const sensors = useStore(s => s.sensorReadings)

  const uniqueIds = Array.from(new Set(sensors.map(r => r.id)))

  const updateValue = async (id: string) => {
    const input = prompt('Nuevo valor para ' + id)
    if (!input) return
    const value = parseFloat(input)
    if (isNaN(value)) return
    try {
      await patchEntity('Sensor', id, { lastValue: value })
      const reading = {
        id,
        property: 'manual',
        value,
        unit: 'C',
        timestamp: new Date().toISOString(),
      }
      useStore.setState(state => {
        const readings = [reading, ...state.sensorReadings]
        return { sensorReadings: readings.slice(0, 10) }
      })
    } catch (err) {
      alert('Error al actualizar')
    }
  }

  return (
    <div>
      <h2 className="font-bold mb-2">Control de Sensores</h2>
      <ul className="space-y-2">
        {uniqueIds.map(id => (
          <li key={id} className="flex items-center gap-2">
            <span className="flex-1">{id}</span>
            <button
              className="px-2 py-1 bg-blue-500 text-white rounded"
              onClick={() => updateValue(id)}
            >
              Actualizar
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
