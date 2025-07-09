import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import SensorTable from '../SensorTable'
import { WebSocketProvider } from '../../utils/ws'

describe('SensorTable', () => {
  it('renders table', () => {
    const { getByText } = render(
      <WebSocketProvider>
        <SensorTable />
      </WebSocketProvider>,
    )
    expect(getByText('Latest Sensors')).toBeTruthy()
  })
})
