# Usar la imagen ligera y eficiente de Nginx basada en Alpine Linux
FROM nginx:alpine

# Metadata del proyecto
LABEL maintainer="I.E. Celmira Bueno de Orejuela"
LABEL description="Smart Menú CBO - Cafetería y Restaurante Escolar Web"
LABEL version="1.0"

# Copiar la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Eliminar el contenido predeterminado de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiar los archivos estáticos de la aplicación web
COPY . /usr/share/nginx/html/

# Exponer el puerto estándar HTTP
EXPOSE 80

# Comprobación de estado (Healthcheck)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Iniciar Nginx en modo primer plano
CMD ["nginx", "-g", "daemon off;"]
