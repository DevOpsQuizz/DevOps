

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

export async function deleteQuestion(id) {
	const url = `${API_BASE}/questions/${id}`
	const adminToken = localStorage.getItem('admin_token')
	const headers = { 'Content-Type': 'application/json' }
	if (adminToken) headers['Authorization'] = `Bearer ${adminToken}`

	const res = await fetch(url, {
		method: 'DELETE',
		headers,
	})
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	return { status: res.status }
}

export async function createQuestion(data) {
	const url = `${API_BASE}/questions/`
	const adminToken = localStorage.getItem('admin_token')
	const headers = { 'Content-Type': 'application/json' }
	if (adminToken) headers['Authorization'] = `Bearer ${adminToken}`

	const res = await fetch(url, {
		method: 'POST',
		headers,
		body: JSON.stringify(data),
	})
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	const contentType = res.headers.get('content-type')
	if (res.status === 204 || !contentType || !contentType.includes('application/json')) {
		return { status: res.status }
	}
	return await res.json()
}

export async function updateQuestion(id, data) {
	const url = `${API_BASE}/questions/${id}`
	const adminToken = localStorage.getItem('admin_token')
	const headers = { 'Content-Type': 'application/json' }
	if (adminToken) headers['Authorization'] = `Bearer ${adminToken}`

	const res = await fetch(url, {
		method: 'PUT',
		headers,
		body: JSON.stringify(data),
	})
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	const contentType = res.headers.get('content-type')
	if (res.status === 204 || !contentType || !contentType.includes('application/json')) {
		return { status: res.status }
	}
	return await res.json()
}

export async function getQuestion(position) {
	const url = `${API_BASE}/questions/${position + 1}`
	const res = await fetch(url)
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	return await res.json()
}

export async function getQuestionsCount() {
	const url = `${API_BASE}/quiz-info`
	const res = await fetch(url)
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	return await res.json()
}

export async function postParticipation(payload) {
	const url = `${API_BASE}/participations`
	const res = await fetch(url, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	})
	if (!res.ok) {
		const txt = await res.text().catch(() => '')
		throw new Error(txt || `HTTP ${res.status}`)
	}
	return await res.json()
}
