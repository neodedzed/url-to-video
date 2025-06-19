function ProductVideo() {
    let product = localStorage.getItem('product')
    const videoUrl = `http://localhost:8000/video/?product=${product}`
    return (
        <> 
            <video controls>
                <source src={videoUrl} type="video/mp4"/>
            </video>
        </>
    )
}

export default ProductVideo