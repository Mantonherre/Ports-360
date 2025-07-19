import { useState } from 'react'
import { login } from '../utils/api'

export default function LoginForm({ onSuccess }: { onSuccess: () => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = await login(username, password)
      localStorage.setItem('token', token)
      setError('')
      onSuccess()
    } catch {
      setError('Error de autenticación')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto space-y-2">
      <div>
        <input
          className="border w-full p-2"
          placeholder="Usuario"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
      </div>
      <div>
        <input
          className="border w-full p-2"
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
      </div>
      {error && <p className="text-red-600">{error}</p>}
      <button className="px-2 py-1 bg-blue-500 text-white rounded" type="submit">
        Entrar
      </button>
    </form>
  )
}
