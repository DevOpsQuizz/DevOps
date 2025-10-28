const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

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
