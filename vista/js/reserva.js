// Variables de control de estado de la reserva
let fechaSeleccionada = "";
let mesaSeleccionada = null;
let metodoPagoSeleccionado = "tarjeta"; // Por defecto

/**
 * MÁSCARA AUTOMÁTICA PARA EL FORMATO DD/MM/YYYY
 */
function mascaraFecha(input) {
    let v = input.value.replace(/\D/g, '').slice(0, 8);
    if (v.length >= 5) {
        input.value = `${v.slice(0, 2)}/${v.slice(2, 4)}/${v.slice(4, 8)}`;
    } else if (v.length >= 3) {
        input.value = `${v.slice(0, 2)}/${v.slice(2)}`;
    } else {
        input.value = v;
    }
}

/**
 * CONTROL DE NAVEGACIÓN ENTRE PANTALLAS
 */
function cambiarVista(idVista) {
    document.querySelectorAll('.view').forEach(vista => {
        vista.classList.remove('active');
    });
    
    const vistaActiva = document.getElementById(idVista);
    if (vistaActiva) {
        vistaActiva.classList.add('active');
    }

    const botonMenuTresLineas = document.querySelector('.settings-container');
    if (botonMenuTresLineas) {
        if (idVista === 'view-home' || idVista === '' || !idVista) {
            botonMenuTresLineas.style.display = 'block';
        } else {
            botonMenuTresLineas.style.display = 'none';
        }
    }
}

/**
 * FUNCIÓN PARA GENERAR EL MAPA DE MESAS
 */
function generarMapaMesas() {
    const grid = document.getElementById('mapa-grid');
    if (!grid) return;
    
    grid.innerHTML = ""; 

    const dj = document.createElement('div');
    dj.className = 'dj-set';
    dj.innerText = '🎧 DJ SET';
    grid.appendChild(dj);

    const clasesMesas = ['m-r', 'm-y', 'm-o', 'm-b', 'm-t'];

    for (let i = 1; i <= 30; i++) {
        const mesa = document.createElement('div');
        const claseAleatoria = clasesMesas[Math.floor(Math.random() * clasesMesas.length)];
        
        mesa.className = `mesa ${claseAleatoria}`;
        mesa.innerText = `M-${i}`;
        
        if (i === 4 || i === 12 || i === 19) {
            mesa.classList.add('ocupada');
            mesa.innerText = '❌';
        } else {
            mesa.onclick = function() {
                document.querySelectorAll('.mesa').forEach(m => m.classList.remove('selected'));
                mesa.classList.add('selected');
                mesaSeleccionada = i;
                
                const info = document.getElementById('map-info');
                const txtMesa = document.getElementById('txt-mesas');
                const txtTotal = document.getElementById('txt-total');
                if (info && txtMesa && txtTotal) {
                    txtMesa.innerText = `Mesa Seleccionada: M-${i}`;
                    txtTotal.innerText = `$${(150000).toLocaleString('es-CO')} COP`;
                    info.style.display = 'block';
                }
            };
        }
        grid.appendChild(mesa);
    }
}

/**
 * VALIDACIÓN DE FECHAS EN FORMATO DD/MM/YYYY
 */
function validarFecha(fechaInput) {
    if (!fechaInput || fechaInput.length < 10) {
        return { valido: false, mensaje: "⚠️ Por favor, ingresa una fecha válida (DD/MM/YYYY)." };
    }

    const partes = fechaInput.split('/');
    const dia = parseInt(partes[0], 10);
    const mes = parseInt(partes[1], 10) - 1; 
    const anio = partes[2];

    if (anio.length !== 4 || isNaN(anio)) {
        return { valido: false, mensaje: "⚠️ El año debe tener exactamente 4 dígitos." };
    }

    const fechaReserva = new Date(parseInt(anio, 10), mes, dia);
    
    if (fechaReserva.getFullYear() !== parseInt(anio, 10) || fechaReserva.getMonth() !== mes || fechaReserva.getDate() !== dia) {
        return { valido: false, mensaje: "⚠️ La fecha ingresada no existe en el calendario." };
    }

    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);

    const maxFecha = new Date();
    maxFecha.setHours(0, 0, 0, 0);
    maxFecha.setMonth(maxFecha.getMonth() + 3);

    if (fechaReserva < hoy) {
        return { valido: false, mensaje: "⚠️ No puedes reservar en una fecha pasada." };
    }

    if (fechaReserva > maxFecha) {
        return { valido: false, mensaje: "⚠️ Solo puedes reservar con un máximo de 3 meses de anticipación." };
    }

    return { valido: true, mensaje: "" };
}

/**
 * ACCIÓN DEL BOTÓN CONTINUAR RESERVACIÓN (CON VALIDACIONES COMPLETAS)
 */
function procesarPasoFecha() {
    const inputFecha = document.getElementById('input-fecha').value;
    const inputPersonas = document.getElementById('personas').value;

    // 1. Validar el campo de fecha primero
    const validacionFecha = validarFecha(inputFecha);
    if (!validacionFecha.valido) {
        mostrarFeedback(validacionFecha.mensaje, true);
        return;
    }

    // 2. Validar que digite la cantidad de personas (No permitir vacío)
    if (!inputPersonas || inputPersonas.trim() === "") {
        mostrarFeedback("⚠️ Por favor, digite la cantidad de personas.", true);
        return;
    }

    // 3. Validar el límite estricto de personas (Mínimo 1, Máximo 10)
    const numPersonas = parseInt(inputPersonas, 10);
    if (numPersonas < 1 || numPersonas > 10 || isNaN(numPersonas)) {
        mostrarFeedback("⚠️ Máximo 10 personas por reserva.", true);
        return;
    }

    // Si pasa todos los filtros con éxito
    fechaSeleccionada = inputFecha; 
    mostrarFeedback("", false); 
    
    generarMapaMesas();
    cambiarVista('view-map'); 
}

/**
 * SELECCIÓN DE MÉTODO DE PAGO
 */
function selectPay(elemento, metodo) {
    document.querySelectorAll('.metodo-pago').forEach(item => item.classList.remove('active'));
    elemento.classList.add('active');
    metodoPagoSeleccionado = metodo;
}

/**
 * FINALIZAR PROCESO
 */
function confirmarReservaFinal() {
    if (!mesaSeleccionada) {
        mostrarFeedback("⚠️ Selecciona una mesa en el plano antes de continuar.", true);
        return;
    }

    mostrarFeedback("🎉 ¡Reserva procesada con éxito!", false);
    
    setTimeout(() => {
        window.location.href = "perfil.html"; 
    }, 2500);
}

/**
 * MENSAJES DE FEEDBACK
 */
function mostrarFeedback(mensaje, esError = true) {
    const vistaActiva = document.querySelector('.view.active');
    if (!vistaActiva) return;

    let contenedorFeedback = vistaActiva.querySelector('.feedback-mensaje');

    if (!contenedorFeedback) {
        contenedorFeedback = document.createElement('div');
        contenedorFeedback.className = 'feedback-mensaje';
        const btnAction = vistaActiva.querySelector('.btn-action');
        if (btnAction) {
            btnAction.parentNode.insertBefore(contenedorFeedback, btnAction);
        } else {
            vistaActiva.appendChild(contenedorFeedback);
        }
    }

    if (mensaje === "") {
        contenedorFeedback.style.display = 'none';
        return;
    }

    contenedorFeedback.innerText = mensaje;
    contenedorFeedback.style.display = 'block';
    
    if (esError) {
        contenedorFeedback.style.color = '#ff6b6b';
        contenedorFeedback.style.background = 'rgba(255, 107, 107, 0.1)';
        contenedorFeedback.style.border = '1px solid rgba(255, 107, 107, 0.3)';
    } else {
        contenedorFeedback.style.color = '#46d2da';
        contenedorFeedback.style.background = 'rgba(70, 210, 218, 0.1)';
        contenedorFeedback.style.border = '1px solid rgba(70, 210, 218, 0.3)';
    }
}

function toggleSettings() {
    const menu = document.getElementById('settings-menu');
    if (menu) {
        menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
    }
}

// Iniciar en la pantalla principal
cambiarVista('view-home');