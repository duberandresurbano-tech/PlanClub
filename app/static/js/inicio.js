document.addEventListener("DOMContentLoaded", () => {
    console.log("Menú de Inicio de PlanClub cargado correctamente. 🚀");

    // Solo aplicamos la lógica a los botones que NO sean el de admin
    const botones = document.querySelectorAll(".btn:not(.btn-admin)");

    botones.forEach(boton => {
        boton.addEventListener("click", (e) => {
            e.preventDefault();

            const textoBoton = boton.textContent.toLowerCase().trim();

            if (textoBoton.includes("catálogo") || textoBoton.includes("bebidas")) {
                window.location.href = "/catalogo";
            } 
            else if (textoBoton.includes("reserva") || textoBoton.includes("mesas")) {
                window.location.href = "/reserva";
            } 
            else if (textoBoton.includes("chat") || textoBoton.includes("vip")) {
                window.location.href = "/chat";
            } 
            else if (textoBoton.includes("perfil") || textoBoton.includes("mi cuenta")) {
                window.location.href = "/perfil";
            }
            else if (textoBoton.includes("salir") || textoBoton.includes("cerrar")) {
                window.location.href = "/logout";
            }
            else {
                const hrefDirecto = boton.getAttribute("href");
                if (hrefDirecto && hrefDirecto !== "#") {
                    window.location.href = hrefDirecto;
                }
            }
        });
    });
});
