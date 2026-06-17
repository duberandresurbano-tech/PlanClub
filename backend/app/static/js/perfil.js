document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita que la página se recargue
    
    // Capturar los valores
    const nombre = document.querySelector('input[type="text"]').value;
    const correo = document.querySelector('input[type="email"]').value;
    
    // Aquí usarías 'fetch' para enviar los datos a tu archivo de backend (.py o .php)
    console.log("Guardando datos de:", nombre, correo);
    alert("Cambios guardados correctamente");
});

// Abrir modal
document.querySelector('.edit-icon').onclick = () => {
    document.getElementById('avatarModal').style.display = 'flex';
};

// Cerrar modal
function closeModal() {
    document.getElementById('avatarModal').style.display = 'none';
}

// Seleccionar y aplicar avatar
function selectAvatar(ruta) {
    const avatarPlaceholder = document.querySelector('.avatar-placeholder');
    avatarPlaceholder.style.backgroundImage = `url('${ruta}')`;
    avatarPlaceholder.style.backgroundSize = 'cover';
    closeModal();
}