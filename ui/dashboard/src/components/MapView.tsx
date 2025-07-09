import { MapContainer, TileLayer, Circle, Tooltip } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { useStore } from '../utils/ws'

export default function MapView() {
  const bathy = useStore(s => s.bathyPoints)

  return (
    <MapContainer center={[38.345, -0.481]} zoom={13} className="h-full w-full">
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {bathy.map(point => (
        <Circle
          key={point.id}
          center={[point.location.coordinates[1], point.location.coordinates[0]]}
          radius={100 / Math.max(point.depth_m, 1)}
          pathOptions={{ color: 'blue' }}
        >
          <Tooltip>
            {point.depth_m} m<br />
            {new Date(point.timestamp).toLocaleString()}
          </Tooltip>
        </Circle>
      ))}
    </MapContainer>
  )
}
