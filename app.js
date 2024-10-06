// Importar Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";

// Configuración de Firebase
const firebaseConfig = {
    apiKey: "API_KEY",
    authDomain: "parking-66bb4.firebaseapp.com",
    projectId: "parking-66bb4",
    storageBucket: "parking-66bb4.appspot.com",
    messagingSenderId: "SENDER_ID",
    appId: "APP_ID",
    measurementId: "G-MG0G7HT8YS"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function cargarLugares() {
    const parkingDiv = document.getElementById('parking');
    parkingDiv.innerHTML = ''; // Limpiar el contenido para evitar duplicados

    // Cargar el archivo JSON local con las posiciones
    const response = await fetch('lugares.json');
    const lugares = await response.json();

    // Obtener solo el estado de los lugares desde Firebase
    const querySnapshot = await getDocs(collection(db, "lugares"));
    const estados = {};
    querySnapshot.forEach((doc) => {
        estados[doc.id] = doc.data().estado;
    });

    // Añadir cada lugar a la vista
    lugares.forEach((lugar) => {
        const lugarDiv = document.createElement('div');
        lugarDiv.classList.add('spot');
        lugarDiv.textContent = lugar.id;

        // Cambiar color basado en el estado obtenido de Firebase
        if (estados[lugar.id] === 'ROJO') {
            lugarDiv.classList.add('rojo');
        } else if (estados[lugar.id] === 'VERDE') {
            lugarDiv.classList.add('verde');
        }

        // Calcular tamaño y posición en porcentajes
        const width = lugar.x2 - lugar.x1;
        const height = lugar.y2 - lugar.y1;

        lugarDiv.style.left = lugar.x1 + '%';
        lugarDiv.style.top = lugar.y1 + '%';
        lugarDiv.style.width = width + '%';
        lugarDiv.style.height = height + '%';

        parkingDiv.appendChild(lugarDiv);
    });
}

// Llamar a la función cada 3 segundos solo para actualizar el estado
setInterval(cargarLugares, 3000);
