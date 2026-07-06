<div align="center">
  <img src="/assets/Logo.png" alt="Logo" style="max-width: 100%; height: auto; width: 450px; margin-bottom: 20px;" />
  
  <h1>Proyecto ING-2</h1>
  <p><strong>Sistema de Gestión para Centros de Actividades</strong></p>

  <p style="margin: 15px 0;">
    <img src="https://img.shields.io/badge/estado-en%20desarrollo-yellow?style=flat-square" />
    <img src="https://img.shields.io/badge/licencia-académico-blue?style=flat-square" />
    <img src="https://img.shields.io/badge/universidad-UNLP-orange?style=flat-square" />
  </p>

  <p style="margin-top: 20px;"><strong>Desarrollado por el equipo SYNCRO</strong></p>
</div>

---

## 📖 Descripción del Proyecto

Este repositorio contiene el desarrollo de un sistema de gestión para centros de actividades.  
La aplicación tiene como objetivo facilitar la administración de socios, la reserva de clases y la gestión de pagos en una única plataforma.

---

## 🎯 Objetivos

- Centralizar la gestión de socios  
- Optimizar el proceso de reservas  
- Facilitar la administración de pagos  
- Permitir la escalabilidad del sistema  

---

## 🚀 Funcionalidades

- 📅 Reserva de clases  
- 👥 Gestión de socios  
- 💳 Administración de pagos  
- 📊 Reportes *(en desarrollo)*  

---

## 🛠 Tecnologías

- Backend: Django
- Frontend: Django Templates
- Base de datos: SQLite
- Infraestructura: Docker

---

## ⚙️ Instalación

```bash
git clone https://github.com/ElianDFernandez/INGE-2.git
cd INGE-2
```

**Docker-Django**
```bash
docker compose up -d --build
```

**Base de datos**
```bash
docker compose exec web python manage.py migrate
```

**Comandos utiles**
```bash
docker compose exec web python manage.py --help
```

**(Opcional) Para que Windows cree un "entorno virutal" para que el editor de código no marque errores**
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

Luego, Ctrl + Shift + P -> Python: Select Interpreter -> venv\Scripts\python.exe

```
**Cómo probar Mercado Pago en entorno local (Para el equipo):**
```
 1- Descargar el ejecutable de Ngrok desde ngrok.com (no se instala por requirements).

 2- Autenticar la cuenta corriendo en la terminal: ngrok config add-authtoken [TOKEN_DEL_EQUIPO]

 3- Levantar el túnel apuntando al puerto de Docker: ngrok http 8000

 4- Copiar la URL https://...ngrok-free.app que devuelve la terminal.

 5- En el archivo reservas/views.py, pegar esa URL en la variable url_ngrok para que Mercado Pago permita el retorno automático hacia nuestro entorno local.
 
```