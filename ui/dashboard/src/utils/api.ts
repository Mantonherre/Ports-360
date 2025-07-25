export async function login(username: string, password: string): Promise<string> {
  const base = import.meta.env.VITE_API_BASE || ''
  const resp = await fetch(`${base}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status}`)
  }
  const data = await resp.json()
  return data.access_token
}

export async function patchEntity(type: string, id: string, patch: object): Promise<void> {
  const base = import.meta.env.VITE_API_BASE || ''
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  const token = import.meta.env.VITE_API_TOKEN || localStorage.getItem('token')
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const resp = await fetch(`${base}/api/entities/${type}/${id}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(patch),
  })
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status}`)
  }
}
