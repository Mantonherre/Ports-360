import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import EnergyGauge from '../EnergyGauge'
import { WebSocketProvider } from '../../utils/ws'

describe('EnergyGauge', () => {
  it('renders gauge', () => {
    const { getByText } = render(
      <WebSocketProvider>
        <EnergyGauge />
      </WebSocketProvider>,
    )
    expect(getByText(/State of Charge/i)).toBeTruthy()
  })
})
