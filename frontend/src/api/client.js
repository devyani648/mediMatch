import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: BASE,
  timeout: 20000,
})

export default {
  search: (payload) => client.post('/api/search', payload),
  uploadCase: (formData) => client.post('/api/cases', formData),
  health: () => client.get('/health'),
}
