import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import SensorControls from '../SensorControls'
import { FakeDataProvider } from '../../utils/mock'

describe('SensorControls', () => {
  it('renders controls', () => {
    const { getByText } = render(
      <FakeDataProvider auto={false}>
        <SensorControls />
      </FakeDataProvider>,
    )
    expect(getByText('Control de Sensores')).toBeTruthy()
  })
})
