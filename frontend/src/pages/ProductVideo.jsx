function ProductVideo() {
    let product = localStorage.getItem('product')
    const videoUrl = `http://localhost:8000/video/?product=${product}`
    return (
        <>
            <p>Hello</p>
            <p>There is info about {product}</p>
            <video controls>
                <source src={videoUrl} type="video/mp4"/>
            </video>
        </>
    )
}

export default ProductVideo