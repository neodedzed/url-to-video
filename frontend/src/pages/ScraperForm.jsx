import { useState } from "react"
import '../styles/login.css'
import { scrapeUrl } from "../api/scraperApi"
import { useNavigate } from "react-router-dom"

function ScraperForm() {
    
    let navigate = useNavigate()

    let [urlToBeScraped, setUrlToBeScraped] = useState('') 

    const handleSubmit = (e) => {
        e.preventDefault()

        //Send URL to backend for scraping
        scrapeUrl({url: urlToBeScraped})
        .then((res)=> {
            
            if(res.data.product) {
                localStorage.setItem('product', res.data.product)
                navigate('/productVideo')
            } 
        })
        .catch((error)=>
            console.error('Cannot Scrape', error)
        )
    }

    
    return (
        <>
            <h2>Ad Generator</h2>
            <form onSubmit={handleSubmit} className='form'>
                <input 
                type='text'
                placeholder="URL to be scraped"
                name='urlToBeScraped'
                onChange={(e)=>(setUrlToBeScraped(e.target.value))}    
                />
                <button type='submit'>Submit</button>
            </form>
        </>
    )
}

export default ScraperForm