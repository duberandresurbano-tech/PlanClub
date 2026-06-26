// Variables de control de estado de la reserva global
let fechaSeleccionada = "";
let cantidadPersonas = 0;
let mesasSeleccionadas = []; 
let metodoPagoSeleccionado = "tarjeta"; // Por defecto

/**
 * FUNCIONES PARA MODALES DE CONFIRMACIÓN CON GLASSMORPHISM Y AMARILLO
 */
function mostrarModalConfirmacion(titulo, mensaje, onConfirm) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 99999;
    `;
    
    const modal = document.createElement('div');
    modal.style.cssText = `
        background: rgba(255, 215, 0, 0.15);
        border: 2px solid rgba(255, 215, 0, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
        animation: slideIn 0.3s ease;
        color: #fff;
        font-family: 'Lexend', sans-serif;
    `;
    
    modal.innerHTML = `
        <h2 style="margin-bottom: 15px; color: #FFD700; font-size: 1.5rem; letter-spacing: 2px;">${titulo}</h2>
        <p style="margin-bottom: 25px; color: #fff; font-size: 0.95rem; line-height: 1.6;">${mensaje}</p>
        <div style="display: flex; gap: 10px; justify-content: center;">
            <button class="btn-modal-cancel" style="
                flex: 1;
                padding: 12px 20px;
                background: rgba(100, 100, 100, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: #fff;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            ">CANCELAR</button>
            <button class="btn-modal-confirm" style="
                flex: 1;
                padding: 12px 20px;
                background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%);
                border: none;
                color: #000;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            ">CONFIRMAR</button>
        </div>
    `;
    
    const btnCancel = modal.querySelector('.btn-modal-cancel');
    const btnConfirm = modal.querySelector('.btn-modal-confirm');
    
    btnCancel.onmouseover = () => {
        btnCancel.style.background = "rgba(100, 100, 100, 0.5)";
    };
    btnCancel.onmouseout = () => {
        btnCancel.style.background = "rgba(100, 100, 100, 0.3)";
    };
    
    btnConfirm.onmouseover = () => {
        btnConfirm.style.transform = "scale(1.05)";
        btnConfirm.style.boxShadow = "0 4px 15px rgba(255, 215, 0, 0.4)";
    };
    btnConfirm.onmouseout = () => {
        btnConfirm.style.transform = "scale(1)";
        btnConfirm.style.boxShadow = "none";
    };
    
    btnCancel.onclick = () => {
        overlay.style.animation = "fadeOut 0.3s ease";
        setTimeout(() => overlay.remove(), 300);
    };
    
    btnConfirm.onclick = () => {
        overlay.style.animation = "fadeOut 0.3s ease";
        setTimeout(() => {
            overlay.remove();
            onConfirm();
        }, 300);
    };
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Agregar estilos de animación si no existen
    if (!document.querySelector('style[data-modal-animations]')) {
        const style = document.createElement('style');
        style.setAttribute('data-modal-animations', 'true');
        style.textContent = `
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            @keyframes fadeOut {
                from {
                    opacity: 1;
                }
                to {
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

function mostrarModalExito(titulo, mensaje) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 99999;
    `;
    
    const modal = document.createElement('div');
    modal.style.cssText = `
        background: rgba(255, 215, 0, 0.15);
        border: 2px solid rgba(255, 215, 0, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
        animation: slideIn 0.3s ease;
        color: #fff;
        font-family: 'Lexend', sans-serif;
    `;
    
    modal.innerHTML = `
        <h2 style="margin-bottom: 15px; color: #FFD700; font-size: 1.5rem; letter-spacing: 2px;">${titulo}</h2>
        <p style="margin-bottom: 25px; color: #fff; font-size: 0.95rem; line-height: 1.6;">${mensaje}</p>
        <button class="btn-modal-ok" style="
            width: 100%;
            padding: 12px 20px;
            background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%);
            border: none;
            color: #000;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        ">ACEPTAR</button>
    `;
    
    const btnOk = modal.querySelector('.btn-modal-ok');
    
    btnOk.onmouseover = () => {
        btnOk.style.transform = "scale(1.05)";
        btnOk.style.boxShadow = "0 4px 15px rgba(255, 215, 0, 0.4)";
    };
    btnOk.onmouseout = () => {
        btnOk.style.transform = "scale(1)";
        btnOk.style.boxShadow = "none";
    };
    
    btnOk.onclick = () => {
        overlay.style.animation = "fadeOut 0.3s ease";
        setTimeout(() => overlay.remove(), 300);
    };
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
}

/**
 * 1. INICIALIZACIÓN DE BASE DE DATOS SIMULADA (HISTORIAL DE OCUPACIÓN)
 * Si no existe un historial en el navegador, creamos uno con datos de prueba.
 */
if (!localStorage.getItem('historial_reservas')) {
    const datosInicialesDePrueba = [
        { fecha: "16/06/2026", mesas: [3, 4], personas: 3, total: "$40.000 COP" },
        { fecha: "17/06/2026", mesas: [7, 8, 9], personas: 6, total: "$60.000 COP" }
    ];
    localStorage.setItem('historial_reservas', JSON.stringify(datosInicialesDePrueba));
}

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
 * CONTROL DE NAVEGACIÓN ENTRE PANTALLAS Y RENDERIZADO DINÁMICO
 */
function cambiarVista(idVista) {
    document.querySelectorAll('.view').forEach(vista => {
        vista.classList.remove('active');
    });
    
    const vistaActiva = document.getElementById(idVista);
    if (vistaActiva) {
        vistaActiva.classList.add('active');
    }

    // Mostrar el menú de configuración solo en el Home principal
    const botonMenuTresLineas = document.querySelector('.settings-container');
    if (botonMenuTresLineas) {
        if (idVista === 'view-home' || idVista === '' || !idVista) {
            botonMenuTresLineas.style.display = 'block';
        } else {
            botonMenuTresLineas.style.display = 'none';
        }
    }

    // Si el usuario entra a ver sus reservas, las pintamos desde el localStorage
    if (idVista === 'view-list') {
        renderizarMisReservas();
    }
}

/**
 * PUNTO 1 & 3: GENERACIÓN REALISTA DEL PLANO (10 MESAS COMPLETAS + COMPORTAMIENTO POR FECHA)
 */
function generarMapaMesas() {
    const plano = document.getElementById('mapa-discoteca');
    if (!plano) return;
    
    // Limpiar mesas viejas antes de redibujar
    const mesasExistentes = plano.querySelectorAll('.mesa');
    mesasExistentes.forEach(m => m.remove());
    
    mesasSeleccionadas = []; // Reiniciar carrito de selección

    // Función para obtener el precio según el ID de la mesa
    function getPrecioMesa(mesaId) {
        if (mesaId === 1 || mesaId === 2) {
            return 35000; // VIP amarillas
        } else if (mesaId >= 3 && mesaId <= 6) {
            return 20000; // Zona Baile
        } else if (mesaId >= 7 && mesaId <= 10) {
            return 15000; // Fondo
        }
        return 20000; // Por defecto
    }

    // Función para obtener la capacidad según el ID de la mesa
    function getCapacidadMesa(mesaId) {
        if (mesaId === 1 || mesaId === 2) {
            return { tipo: 'VIP', capacidad: 8 };
        } else if (mesaId >= 3 && mesaId <= 6) {
            return { tipo: 'Zona Baile', capacidad: 6 };
        } else if (mesaId >= 7 && mesaId <= 10) {
            return { tipo: 'Fondo', capacidad: 4 };
        }
        return { tipo: 'Estándar', capacidad: 4 };
    }

    // Obtener las reservas existentes desde el LocalStorage para saber cuáles bloquear hoy
    const historial = JSON.parse(localStorage.getItem('historial_reservas')) || [];
    
    // Buscamos si hay registros de ocupación específicamente para la fecha seleccionada
    const reservaDelDia = historial.find(r => r.fecha === fechaSeleccionada);
    // Si encontramos reservas, extraemos los números de las mesas ocupadas; si no, queda vacío []
    const mesasOcupadasHoy = reservaDelDia ? reservaDelDia.mesas : [];

    // Coordenadas premium en porcentaje para ubicar de forma envolvente las 10 mesas libres
    const posiciones = [
        { id: 1, x: 8, y: 28 },    // Lateral Izquierdo Alto
        { id: 2, x: 84, y: 28 },   // Lateral Derecho Alto
        { id: 3, x: 10, y: 54 },   // Lateral Izquierdo Medio
        { id: 6, x: 82, y: 54 },   // Lateral Derecho Medio
        { id: 7, x: 16, y: 78 },   // Lateral Izquierdo Bajo
        { id: 10, x: 76, y: 78 },  // Lateral Derecho Bajo
        { id: 8, x: 34, y: 88 },   // Curva Inferior Izquierda
        { id: 9, x: 58, y: 88 },   // Curva Inferior Derecha
        { id: 4, x: 36, y: 54 },   // Frente de pista VIP Izquierda
        { id: 5, x: 56, y: 54 }    // Frente de pista VIP Derecha
    ];

    positions = posiciones.forEach((pos, index) => {
        const mesa = document.createElement('div');
        
        // Asignar clases por rango de ID
        let claseColor;
        if (pos.id === 1 || pos.id === 2) {
            claseColor = 'm-y'; 
        } else if (pos.id >= 3 && pos.id <= 6) {
            claseColor = 'm-b'; 
        } else if (pos.id >= 7 && pos.id <= 10) {
            claseColor = 'm-t'; 
        }
        
        mesa.className = `mesa ${claseColor}`;
        mesa.innerText = `M-${pos.id}`;
        
        mesa.style.left = `${pos.x}%`;
        mesa.style.top = `${pos.y}%`;
        
        // CONDICIONAL DINÁMICA: Si la mesa está guardada como ocupada en esta fecha
        if (mesasOcupadasHoy.includes(pos.id)) {
            mesa.classList.add('ocupada');
            mesa.innerText = '❌';
        } else {
            // Mesa libre disponible para interactuar
            mesa.onclick = function() {
                mostrarFeedback("", false); // Limpiar errores visuales previos

                // Regala 1: De 1 a 4 personas -> Solo permite 1 mesa única
                if (cantidadPersonas <= 4) {
                    document.querySelectorAll('.mesa').forEach(m => m.classList.remove('selected'));
                    mesasSeleccionadas = [pos.id];
                    mesa.classList.add('selected');
                } 
                // Regla 2: De 5 a 10 personas -> Selección múltiple con tope estricto de 4
                else {
                    if (mesasSeleccionadas.includes(pos.id)) {
                        mesasSeleccionadas = mesasSeleccionadas.filter(id => id !== pos.id);
                        mesa.classList.remove('selected');
                    } else {
                        if (mesasSeleccionadas.length >= 4) {
                            mostrarFeedback("⚠️ El maximo de mesas permitido por reserva es de 4.", true);
                            return; 
                        }
                        mesasSeleccionadas.push(pos.id);
                        mesa.classList.add('selected');
                    }
                }
                
                // Actualizar desglose de cobro en pantalla
                const info = document.getElementById('map-info');
                const txtMesa = document.getElementById('txt-mesas');
                const txtTotal = document.getElementById('txt-total');
                
                if (info && txtMesa && txtTotal) {
                    if (mesasSeleccionadas.length > 0) {
                        const mesasInfo = mesasSeleccionadas.map(id => {
                            const cap = getCapacidadMesa(id);
                            return `M-${id} (${cap.tipo}: ${cap.capacidad} personas)`;
                        }).join(', ');
                        txtMesa.innerText = `Mesas reservadas: ${mesasInfo}`;
                        let totalCalculado = mesasSeleccionadas.reduce((sum, mesaId) => sum + getPrecioMesa(mesaId), 0);
                        txtTotal.innerText = `$${totalCalculado.toLocaleString('es-CO')} COP`;
                        info.style.display = 'block';
                    } else {
                        info.style.display = 'none';
                    }
                }
            };
        }
        plano.appendChild(mesa);
    });
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
 * ACCIÓN DEL BOTÓN CONTINUAR RESERVACIÓN
 */
function procesarPasoFecha() {
    let inputFecha = document.getElementById('input-fecha').value;
    const inputPersonas = document.getElementById('personas').value;

    // Convertir formato de date input (YYYY-MM-DD) a DD/MM/YYYY
    if (inputFecha && inputFecha.includes('-')) {
        const [anio, mes, dia] = inputFecha.split('-');
        inputFecha = `${dia}/${mes}/${anio}`;
    }

    const validacionFecha = validarFecha(inputFecha);
    if (!validacionFecha.valido) {
        mostrarFeedback(validacionFecha.mensaje, true);
        return;
    }

    if (!inputPersonas || inputPersonas.trim() === "") {
        mostrarFeedback("⚠️ Por favor, digite la cantidad de personas.", true);
        return;
    }

    const numPersonas = parseInt(inputPersonas, 10);
    if (numPersonas < 1 || numPersonas > 10 || isNaN(numPersonas)) {
        mostrarFeedback("⚠️ Máximo 10 personas por reserva.", true);
        return;
    }

    fechaSeleccionada = inputFecha; 
    cantidadPersonas = numPersonas; 
    
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
 * PUNTO 2 & 3: PROCESAR PAGO Y PERSISTENCIA DE DATOS LOCALES
 */
function confirmarReservaFinal() {
    if (mesasSeleccionadas.length === 0) {
        mostrarFeedback("⚠️ Selecciona al menos una mesa en el plano antes de continuar.", true);
        return;
    }

    const totalTexto = document.getElementById('txt-total').innerText;
    const historial = JSON.parse(localStorage.getItem('historial_reservas')) || [];
    
    const registroExistente = historial.find(r => r.fecha === fechaSeleccionada);
    if (registroExistente) {
        registroExistente.mesas = [...registroExistente.mesas, ...mesasSeleccionadas];
    } else {
        historial.push({
            fecha: fechaSeleccionada,
            mesas: mesasSeleccionadas,
            personas: cantidadPersonas,
            total: totalTexto
        });
    }
    
    localStorage.setItem('historial_reservas', JSON.stringify(historial));

    mostrarFeedback("🎉 ¡Reserva procesada con éxito!", false);
    
    // 🛠️ CORREGIDO: Redirección limpia al endpoint lógico de Flask para reiniciar la vista
    setTimeout(() => {
        window.location.href = "/reserva"; 
    }, 2500);
}

function renderizarMisReservas() {
    const contenedor = document.getElementById('reserva-container');
    if (!contenedor) return;

    contenedor.innerHTML = ""; 
    const historial = JSON.parse(localStorage.getItem('historial_reservas')) || [];

    // --- BOTÓN PARA BORRAR TODO ---
    const btnReset = document.createElement('button');
    btnReset.innerText = "🗑️ BORRAR TODAS";
    btnReset.className = "btn-delete-all";
    btnReset.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999999;
        padding: 12px 18px;
        background: linear-gradient(135deg, #ff3c3c 0%, #ff6b5b 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 60, 60, 0.3);
        letter-spacing: 0.5px;
    `;
    
    btnReset.onmouseover = () => {
        btnReset.style.boxShadow = "0 6px 25px rgba(255, 60, 60, 0.6)";
        btnReset.style.transform = "translateY(-2px)";
    };
    
    btnReset.onmouseout = () => {
        btnReset.style.boxShadow = "0 4px 15px rgba(255, 60, 60, 0.3)";
        btnReset.style.transform = "translateY(0)";
    };
    
    btnReset.onclick = function(e) {
        e.preventDefault();
        mostrarModalConfirmacion(
            "¿Estás 100% seguro?",
            "Esto eliminará TODAS las reservas y dejará todas las mesas libres.",
            function() {
                localStorage.removeItem('historial_reservas');
                localStorage.setItem('historial_reservas', JSON.stringify([]));
                mostrarModalExito("✅ Éxito", "Todas las reservas fueron eliminadas correctamente.");
                setTimeout(() => location.reload(), 1500);
            }
        );
    };
    document.body.appendChild(btnReset);
    // ------------------------------------

    if (historial.length === 0) {
        contenedor.innerHTML = `<p style="text-align:center; color:#888; padding:20px;">No tienes reservas registradas.</p>`;
        return;
    }

    historial.forEach(res => {
        const tarjeta = document.createElement('div');
        tarjeta.className = 'card';
        tarjeta.innerHTML = `
            <p>📅 Fecha: ${res.fecha}</p>
            <p>Mesa(s): ${res.mesas.join(', ')}</p>
            <p>Total: ${res.total}</p>
        `;
        contenedor.appendChild(tarjeta);
    });
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

// Iniciar aplicación en la visual Home
cambiarVista('view-home');