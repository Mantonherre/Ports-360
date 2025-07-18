import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import SensorTable from '../SensorTable'
import { FakeDataProvider } from '../../utils/mock'

describe('SensorTable', () => {
  it('renders table', () => {
    const { getByText } = render(
      <FakeDataProvider>
        <SensorTable />
      </FakeDataProvider>,
    )
    expect(getByText('Latest Sensors')).toBeTruthy()
  })
})
