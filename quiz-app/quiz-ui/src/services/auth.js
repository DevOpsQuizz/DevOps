const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function loginAdmin(password) {
  const url = `${API_BASE}/auth/login`
  console.log('POST ->', url)
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(txt || `HTTP ${res.status}`)
  }
  return (await res.json()).token
}