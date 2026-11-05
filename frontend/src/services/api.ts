import axios from 'axios'

/**
 * Reads a cookie value by name (used for Django CSRF token).
 */
export function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null
  const match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'))
  return match ? decodeURIComponent(match[3]) : null
}

/**
 * Pre-configured Axios instance for the LITAN API:
 * - baseURL: '/api' (proxied by Nginx in prod and Vite in dev)
 * - withCredentials: true (transmits session cookies on same-origin requests)
 * - X-CSRFToken header automatically attached on mutations
 */
export const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: attach CSRF token if present
api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken')
  if (csrfToken && config.headers) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

// Response interceptor: handle 401 / 403 gracefully
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // User is unauthenticated
    }
    return Promise.reject(error)
  }
)

export default api
