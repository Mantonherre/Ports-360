import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import EnergyGauge from '../EnergyGauge'
import { FakeDataProvider } from '../../utils/mock'

describe('EnergyGauge', () => {
  it('renders gauge', () => {
    const { getByText } = render(
      <FakeDataProvider>
        <EnergyGauge />
      </FakeDataProvider>,
    )
    expect(getByText(/State of Charge/i)).toBeTruthy()
  })
})
