import api from '../api/axiosConfig'

export const scrapeUrl = (params) => {
    return api.post('/scraper', params) 
}