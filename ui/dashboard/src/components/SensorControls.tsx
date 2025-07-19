import { useStore } from '../utils/mock'
import { patchEntity } from '../utils/api'

export default function SensorControls() {
  const sensors = useStore(s => s.sensorReadings)
  const addSensor = useStore(s => s.addSensor)
  const updateSensor = useStore(s => s.updateSensor)
  const removeSensor = useStore(s => s.removeSensor)

  const uniqueIds = Array.from(new Set(sensors.map(r => r.id)))

  const updateValue = async (id: string) => {
    const input = prompt('Nuevo valor para ' + id)
    if (!input) return
    const value = parseFloat(input)
    if (isNaN(value)) return
    try {
      await patchEntity('Sensor', id, { lastValue: value })
      updateSensor(id, value)
    } catch (err) {
      alert('Error al actualizar')
    }
  }

  const createSensor = async () => {
    const id = prompt('ID del nuevo sensor')
    if (!id) return
    const valStr = prompt('Valor inicial')
    if (!valStr) return
    const value = parseFloat(valStr)
    if (isNaN(value)) return
    try {
      await patchEntity('Sensor', id, { lastValue: value })
      addSensor(id, value)
    } catch (err) {
      alert('Error al crear')
    }
  }

  const deleteSensor = (id: string) => {
    removeSensor(id)
  }

  return (
    <div>
      <h2 className="font-bold mb-2">Control de Sensores</h2>
      <div className="mb-2">
        <button
          className="px-2 py-1 bg-green-600 text-white rounded"
          onClick={createSensor}
        >
          Crear Sensor
        </button>
      </div>
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
            <button
              className="px-2 py-1 bg-red-500 text-white rounded"
              onClick={() => deleteSensor(id)}
            >
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
