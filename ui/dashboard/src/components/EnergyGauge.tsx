import { RadialBarChart, RadialBar } from 'recharts'
import { useStore } from '../utils/ws'

export default function EnergyGauge() {
  const soc = useStore(s => s.stateOfCharge)

  const data = [{ name: 'SOC', value: soc }]

  return (
    <div className="text-center">
      <h2 className="font-bold mb-2">Battery State of Charge</h2>
      <RadialBarChart width={200} height={200} innerRadius="80%" outerRadius="100%" data={data} startAngle={180} endAngle={0}>
        <RadialBar dataKey="value" minAngle={15} clockWise fill="#8884d8" />
      </RadialBarChart>
      <p className="text-xl">{soc}%</p>
    </div>
  )
}
