// const apiUrl = 'http://127.0.0.1:5000'
const apiUrl = process.env.NODE_ENV === 'production' ? 'https://tfm-anmarlea-upv-15.appspot.com/' : 'http://127.0.0.1:5000'

export default apiUrl
