export const BACKEND_URL = (process.env.REACT_APP_BACKEND_URL) ? (
    "http://" + process.env.REACT_APP_BACKEND_URL
) : (
    window.location.origin + "/api"
)
