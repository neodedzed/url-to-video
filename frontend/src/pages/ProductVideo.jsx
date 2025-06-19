function ProductVideo() {
    let product = localStorage.getItem('product')
    return (
        <>
            <p>Hello</p>
            <p>There is info about {product}</p>
        </>
    )
}

export default ProductVideo