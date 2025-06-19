import { useState } from "react"
import { scrapeUrl } from "../api/scraperApi"

function ScraperForm() {
    let [urlToBeScraped, setUrlToBeScraped] = useState('') 
    const handleSubmit = (e) => {
        e.preventDefault()

        //Send URL to backend for scraping
        scrapeUrl({url: urlToBeScraped})
        .then((res)=>
            console.log(res.data)
        )
        .catch((error)=>
            console.error('Cannot Scrape', error)
        )
    }

    
    return (
        <>
            <form onSubmit={handleSubmit}>
                <input 
                type='text'
                name='urlToBeScraped'
                onChange={(e)=>(setUrlToBeScraped(e.target.value))}    
                />
                <button type='submit'>Submit</button>
            </form>
        </>
    )
}

export default ScraperForm