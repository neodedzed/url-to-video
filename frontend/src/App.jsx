import { Route, Routes } from 'react-router-dom'
import './App.css'
import ScraperForm from './pages/ScraperForm'
import ProductVideo from './pages/ProductVideo'

function App() {
  return (
    <>
      <Routes>
        <Route path='/' element= {<ScraperForm />}/>
        <Route path='/productVideo' element= {<ProductVideo />}/>
      </Routes>
    </>
  )
}

export default App
