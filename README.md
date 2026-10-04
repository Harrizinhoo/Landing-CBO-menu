# Smart Menú CBO - Cafetería y Restaurante Escolar

Sitio web oficial interactivo para el restaurante y cafetería escolar de la **Institución Educativa Celmira Bueno de Orejuela (CBO)**, Cali.

---

## 🍽️ Descripción del Proyecto

Smart Menú CBO es una plataforma web desarrollada para exhibir el menú diario y semanal de desayunos, almuerzos y refrigerios saludables ofrecidos a la comunidad educativa, promoviendo hábitos alimenticios saludables y transparencia nutricional.

---

## 🐳 Ejecución con Docker

### Opción 1: Construcción y ejecución directa con Docker
```bash
# 1. Construir la imagen
docker build -t smart-menu-cbo-web:1.0 .

# 2. Correr el contenedor en el puerto 8080
docker run -d --name smart_menu_cbo_app -p 8080:80 smart-menu-cbo-web:1.0

# 3. Abrir en el navegador
http://localhost:8080
```

### Opción 2: Usar Docker Compose
```bash
# Iniciar contenedor
docker-compose up -d

# Detener contenedor
docker-compose down
```

---

## 🚀 Despliegue en GitHub Pages

El proyecto incluye el flujo automatizado de **GitHub Actions** en `.github/workflows/deploy.yml`.

### Pasos para activar el dominio permanente en GitHub Pages:
1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a tu repositorio en GitHub > **Settings** > **Pages**.
3. En **Build and deployment** > **Source**, selecciona **GitHub Actions**.
4. ¡Listo! Tu sitio web estará disponible de forma permanente y con certificado HTTPS gratuito en:
   ```text
   https://<tu-usuario-de-github>.github.io/<nombre-del-repositorio>/
   ```
