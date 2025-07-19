import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import MapView from '../MapView'
import { FakeDataProvider } from '../../utils/mock'

describe('MapView', () => {
  it('renders without crashing', () => {
    render(
      <FakeDataProvider auto={false}>
        <div style={{ height: 400 }}>
          <MapView />
        </div>
      </FakeDataProvider>,
    )
    expect(true).toBe(true)
  })
})
