import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import MapView from '../MapView'
import { WebSocketProvider } from '../../utils/ws'

describe('MapView', () => {
  it('renders without crashing', () => {
    render(
      <WebSocketProvider>
        <div style={{ height: 400 }}>
          <MapView />
        </div>
      </WebSocketProvider>,
    )
    expect(true).toBe(true)
  })
})
