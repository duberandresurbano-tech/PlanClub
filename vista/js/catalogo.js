// ==========================================================================
// SIMULACIÓN DE TU BASE DE DATOS (bdProductos)
// Si una categoría se queda vacía [], el script mostrará la pantalla en gris.
// ==========================================================================
let bdProductos = [
    { nombre: 'Bacardi', precio: 70000, cat: 'bebidas', img: 'https://cdn.mos.cms.futurecdn.net/v2/t:0,l:218,cw:563,ch:563,q:80,w:563/wn2NRMm5iJBXeZPBrefnhK.jpg' },
    { nombre: 'Coronita', precio: 5000, cat: 'bebidas', img: 'https://i.pinimg.com/474x/82/d8/48/82d84883fb32e2e4c31c7760830ee0f1.jpg' },
    { nombre: 'Néctar', precio: 50000, cat: 'bebidas', img: 'https://pbs.twimg.com/profile_images/472153934015254529/XOrYqyI2_400x400.jpeg' },
    { nombre: 'Poker', precio: 3500, cat: 'bebidas', img: 'https://images.seeklogo.com/logo-png/18/1/cerveza-poker-logo-png_seeklogo-184736.png' },
    { nombre: 'aguila', precio: 3500, cat: 'bebidas', img: 'https://imgproxy.domestika.org/unsafe/rs:fill/plain/src://content-items/002/864/382/Aguila_logo-original.png?1552905177' },
    { nombre: 'powerade', precio: 5000, cat: 'bebidas', img: 'https://logowik.com/content/uploads/images/powerade374.logowik.com.webp' },
    { nombre: 'aguardiente amarillo', precio: 50000, cat: 'bebidas', img: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0ro27SpW_X4XaTzLFQB2BWwNb80we3Kj9Ng&s' },
    { nombre: 'ron viejo de caldas', precio: 62000, cat: 'bebidas', img: 'https://www.ronviejodecaldasrum.com/image/5862128.1593880979000/ronviego_logo_RED_W_RED_STROKE_540X410_300_O.png' }
];

// Estado global de la aplicación
let carrito = [];
let filtroActivo = 'bebidas'; // Categoría inicial

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    renderizarCatalogo();
});

// ==========================================================================
// RENDERIZAR PRODUCTOS O MOSTRAR ESTADO EN GRIS
// ==========================================================================
function renderizarCatalogo() {
    // Apuntamos al contenedor interno dinámico que creamos en el HTML
    const contenedor = document.getElementById('contenedor-productos-dinamicos');
    if (!contenedor) return;
    
    contenedor.innerHTML = '';

    // Filtramos los productos según la categoría activa
    const productosFiltrados = bdProductos.filter(p => p.cat === filtroActivo);

    // Si la base de datos no arroja productos para esta categoría -> Pantalla en gris
    if (productosFiltrados.length === 0) {
        contenedor.innerHTML = `
            <div style="text-align: center; padding: 60px 20px; color: #555566; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 350px;">
                <span style="font-size: 64px; filter: grayscale(1); opacity: 0.3; margin-bottom: 15px; display: block; animation: reboteSuave 1.5s infinite alternate ease-in-out;">🥂</span>
                <h3 style="font-size: 16px; font-weight: 700; color: #8e8e93; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">Catálogo No Disponible</h3>
                <p style="font-size: 13px; color: #636366; max-width: 220px; line-height: 1.4;">Por el momento no tenemos productos en esta sección.</p>
            </div>
        `;
        return;
    }

    // Si tiene productos, dibuja el título de la sección
    const tituloSec = document.createElement('div');
    tituloSec.className = 'section-title';
    tituloSec.innerText = filtroActivo.toUpperCase();
    contenedor.appendChild(tituloSec);

    // Creamos la cuadrícula de productos
    const grid = document.createElement('div');
    grid.className = 'products'; // Usa la clase CSS nativa de tu diseño

    productosFiltrados.forEach(prod => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="${prod.img}" alt="${prod.nombre}">
            <p>${prod.nombre}</p>
            <p class="price">$${prod.precio.toLocaleString('es-CO')}</p>
            <button class="add-btn" onclick="agregar('${prod.nombre}', ${prod.precio})">+</button>
        `;
        grid.appendChild(card);
    });
    
    contenedor.appendChild(grid);
}

// ==========================================================================
// LÓGICA DEL CARRITO Y PEDIDOS
// ==========================================================================

function agregar(nombre, precio) {
    // Añade el producto seleccionado al arreglo del carrito
    carrito.push({ nombre, precio });
    actualizarInterfazCarrito();
}

function actualizarInterfazCarrito() {
    // Actualiza el contador numérico del botón de navegación inferior
    const contador = document.getElementById('cart-count');
    if (contador) contador.innerText = carrito.length;

    // Actualiza la lista visual interna de la sección "MI PEDIDO"
    const listaPedido = document.getElementById('listaPedido');
    const totalSpan = document.getElementById('total');
    
    if (listaPedido) {
        listaPedido.innerHTML = '';
        let sumaTotal = 0;

        carrito.forEach((item, index) => {
            sumaTotal += item.precio;
            const itemElemento = document.createElement('div');
            itemElemento.style.cssText = "display:flex; justify-content:between; padding:10px; border-bottom:1px solid #333; color:#fff;";
            itemElemento.innerHTML = `
                <span style="flex:1;">${item.nombre}</span>
                <span style="margin-right:15px;">$${item.precio.toLocaleString('es-CO')}</span>
                <button onclick="eliminarDelCarrito(${index})" style="background:none; border:none; color:#ff453a; cursor:pointer;">✕</button>
            `;
            listaPedido.appendChild(itemElemento);
        });

        if (totalSpan) totalSpan.innerText = sumaTotal.toLocaleString('es-CO');
    }
}

function eliminarDelCarrito(index) {
    carrito.splice(index, 1);
    actualizarInterfazCarrito();
}

function vaciarCarrito() {
    carrito = [];
    actualizarInterfazCarrito();
    regresar();
}

// ==========================================================================
// NAVEGACIÓN Y MODALES
// ==========================================================================

function verPedido() {
    document.getElementById('catalogo-screen').style.display = 'none';
    document.getElementById('pedido').style.display = 'block';
    document.getElementById('main-nav').style.display = 'none';
}

function regresar() {
    // Cierra modales u oculta la pantalla de pedidos
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('modal-confirmacion').style.display = 'block';
    document.getElementById('modal-gracias').style.display = 'none';
    
    document.getElementById('pedido').style.display = 'none';
    document.getElementById('catalogo-screen').style.display = 'block';
    document.getElementById('main-nav').style.display = 'flex';
}

function abrirConfirmacion() {
    if (carrito.length === 0) {
        alert("Tu carrito está vacío.");
        return;
    }
    document.getElementById('overlay').style.display = 'flex';
}

function procesarPedido() {
    document.getElementById('modal-confirmacion').style.display = 'none';
    document.getElementById('modal-gracias').style.display = 'block';
}

function reiniciarApp() {
    carrito = [];
    actualizarInterfazCarrito();
    regresar();
}
