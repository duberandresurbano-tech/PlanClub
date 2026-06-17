// Variable global temporal para guardar la foto seleccionada en el modal antes de aceptar
let fotoTemporalSeleccionada = "";

// --- MODAL DE NOTIFICACIONES ---
function openNotificationModal() {
    const modal = document.getElementById('notificationModal');
    if (modal) modal.style.display = 'flex';
}

function closeNotificationModal() {
    const modal = document.getElementById('notificationModal');
    if (modal) modal.style.display = 'none';
}

// --- MODAL DE FOTO DE PERFIL ---
function openPhotoModal() {
    const modal = document.getElementById('photoEditModal');
    if (modal) {
        modal.style.display = 'flex';
        // Limpiamos selecciones previas visuales dentro del modal
        document.querySelectorAll('.profile-option').forEach(opt => opt.classList.remove('selected'));
        fotoTemporalSeleccionada = ""; 
    }
}

function closePhotoModal() {
    const modal = document.getElementById('photoEditModal');
    if (modal) modal.style.display = 'none';
}

// Al hacer clic en una de las fotos del grid (a.jpg, b.jpg, c.jpg)
function selectPhoto(elemento) {
    // Quitamos el borde resaltado de las otras opciones
    document.querySelectorAll('.profile-option').forEach(opt => opt.classList.remove('selected'));
    
    // Añadimos el resaltado a la foto cliqueada
    elemento.classList.add('selected');
    
    // Capturamos la ruta que guardamos en el atributo 'data-photo-src'
    fotoTemporalSeleccionada = elemento.getAttribute('data-photo-src');
}

// Al darle al botón "ACEPTAR" dentro del modal de fotos
function applyPhotoChange() {
    if (!fotoTemporalSeleccionada) {
        alert("⚠️ Por favor, selecciona una foto antes de aceptar.");
        return;
    }
    
    const contenedorFoto = document.getElementById('mainProfilePic');
    if (contenedorFoto) {
        // Cambiamos el icono de FontAwesome por la imagen real de fondo
        contenedorFoto.innerHTML = ""; // Borra el <i class="fa-solid fa-user"></i>
        contenedorFoto.style.backgroundImage = `url('${fotoTemporalSeleccionada}')`;
        contenedorFoto.style.backgroundSize = 'cover';
        contenedorFoto.style.backgroundPosition = 'center';
    }
    
    closePhotoModal();
}

// --- GUARDAR DATOS DEL FORMULARIO ---
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita que la página se recargue
    
    const nombre = document.querySelector('input[placeholder="Escribe tu nombre"]').value.trim();
    const apellido = document.querySelector('input[placeholder="Escribe tu apellido"]').value.trim();
    const correo = document.querySelector('input[placeholder="ejemplo@correo.com"]').value.trim();
    const telefono = document.querySelector('input[placeholder="Tu número"]').value.trim();
    
    console.log("Datos listos para enviar a la BD:", { nombre, apellido, correo, telefono });
    alert("¡Cambios guardados correctamente en tu perfil!");
});