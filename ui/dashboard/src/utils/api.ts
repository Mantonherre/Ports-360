export async function patchEntity(type: string, id: string, patch: object): Promise<void> {
  const base = import.meta.env.VITE_API_BASE || ''
  const resp = await fetch(`${base}/api/entities/${type}/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(patch),
  })
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status}`)
  }
}
