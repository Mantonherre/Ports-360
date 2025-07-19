import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import LoginForm from '../LoginForm'

describe('LoginForm', () => {
  it('renders form', () => {
    const { getByText } = render(<LoginForm onSuccess={() => {}} />)
    expect(getByText('Entrar')).toBeTruthy()
  })
})
