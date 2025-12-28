async function loadProducts() {
    const res = await fetch('/api/products/');
    const data = await res.json();
    const container = document.getElementById('products');

    data.forEach(p => {
        const card = document.createElement('div');
        card.innerHTML = 
            <img src="${p.image}" width="200">
            <h3>${p.name}</h3>
            <p>${p.price} تومان</p>
        ;
        container.appendChild(card);
    });
}
loadProducts();