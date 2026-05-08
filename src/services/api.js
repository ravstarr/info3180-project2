const API_BASE_URL = 'http://127.0.0.1:5001'

export const apiFetch = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include', 
    ...options
  })

  let data
  try {
    data = await response.json()
  } catch {
    data = {}
  }

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Request failed')
  }

  return data
}