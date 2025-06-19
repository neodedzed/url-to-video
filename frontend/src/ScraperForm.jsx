import { useState } from "react"

function ScraperForm() {
    let [urlToBeScraped, setUrlToBeScraped] = useState('') 
    const handleSubmit = (e) => {
        e.preventDefault()
        console.log(urlToBeScraped)
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