# BruteForcing Login Script

## Descripción

Este script realiza un ataque de fuerza bruta en formularios de inicio de sesión utilizando combinaciones de nombres de usuario y contraseñas desde archivos externos. Fue diseñado con fines **puramente académicos** para resolver retos como los ofrecidos en plataformas como PortSwigger. **No está diseñado ni debe usarse para actividades maliciosas.**

## Características

- Soporte multithreading para pruebas rápidas.
- Barra de progreso interactiva con `tqdm` para monitorear el progreso.
- Configurable mediante argumentos para personalizar la URL, usuarios, contraseñas y la cadena que indica éxito.
- Detecta credenciales válidas y se detiene inmediatamente.

## Requisitos

- Python 3.7 o superior.
- Conexión estable a Internet para probar en servidores remotos.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/bruteforcing-login.git
   cd bruteforcing-login
   ```
2. Instala las dependencias desde `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## requirements.txtUso

Ejemplo de ejecución:

```bash
python3 bruteforcing.py -u https://0afd0011041996c083120ad600620054.web-security-academy.net/login \
  -us usuarios_noborrar.txt -pw passwords_db.txt -s "My Account"
```

### Argumentos

- `-u`, `--url`: URL del formulario de login objetivo.
- `-us`, `--user-file`: Archivo con la lista de usuarios (uno por línea).
- `-pw`, `--password-file`: Archivo con la lista de contraseñas (una por línea).
- `-s`, `--success-string`: Cadena que indica un login exitoso (por ejemplo: "My Account").

### Recomendaciones

- Si el script no puede apagarse con `Ctrl + C`, haz un kill a la terminal para detenerlo completamente. Este comportamiento puede ser corregido en futuras versiones.

### Limitaciones

- **No usar en sitios web con protecciones avanzadas:** Este script no está diseñado para manejar bloqueos automáticos tras múltiples intentos fallidos (e.g., bloqueos por IP o CAPTCHA).
- **Fines educativos:** Fue desarrollado como parte de un reto académico y no debe utilizarse en entornos no autorizados.

## Dependencias

El script utiliza las siguientes librerías de Python:

- `argparse`: Para manejar argumentos desde la línea de comandos.
- `requests`: Para enviar peticiones HTTP/S.
- `tqdm`: Para mostrar barras de progreso.
- `concurrent.futures`: Para implementar multithreading.
- `signal` y `sys`: Para manejar interrupciones como `Ctrl + C`.

Estas dependencias se encuentran en el archivo `requirements.txt`.

## Archivo `requirements.txt`

```plaintext
argparse
requests
tqdm
```

## Descargo de responsabilidad

Este script fue creado exclusivamente con fines educativos y para pruebas en entornos controlados y autorizados. **No nos hacemos responsables del mal uso del mismo.** Asegúrate de contar con permisos explícitos antes de realizar pruebas de seguridad en cualquier sistema.

