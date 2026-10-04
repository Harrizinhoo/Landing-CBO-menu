"""
Script automatizado para crear el repositorio en GitHub y subir todos los archivos
utilizando la API REST de GitHub (sin necesidad de Git CLI instalado).
"""
import os
import sys
import base64
import json
import urllib.request
import urllib.error

def upload_project(github_username, github_token, repo_name="smart-menu-cbo-web"):
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "SmartMenuCBO-Deployer"
    }

    print(f"[*] Verificando/Creando repositorio '{repo_name}' en la cuenta de @{github_username}...")
    
    # 1. Crear repositorio si no existe
    create_repo_url = "https://api.github.com/user/repos"
    payload = {
        "name": repo_name,
        "description": "Smart Menú CBO - Cafetería y Restaurante Escolar (I.E. Celmira Bueno de Orejuela)",
        "private": False,
        "auto_init": False
    }

    req = urllib.request.Request(create_repo_url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print("[+] Repositorio creado exitosamente.")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print("[i] El repositorio ya existe en tu cuenta. Se continuará con la sincronización.")
        else:
            print(f"[-] Error al crear repositorio: {e.code} - {e.read().decode()}")
            return False

    # 2. Recorrer archivos y subirlos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ignored = {'.git', '__pycache__', 'deploy_to_github.py'}
    
    print("[*] Subiendo archivos del proyecto a GitHub...")
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for file in files:
            if file in ignored:
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_dir).replace('\\', '/')
            
            with open(full_path, 'rb') as f:
                content_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Obtener SHA si ya existe
            file_url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/{rel_path}"
            sha = None
            try:
                check_req = urllib.request.Request(file_url, headers=headers)
                with urllib.request.urlopen(check_req) as check_resp:
                    data = json.loads(check_resp.read().decode())
                    sha = data.get('sha')
            except urllib.error.HTTPError:
                pass
            
            upload_payload = {
                "message": f"Subir {rel_path}",
                "content": content_b64
            }
            if sha:
                upload_payload["sha"] = sha
                
            put_req = urllib.request.Request(file_url, data=json.dumps(upload_payload).encode('utf-8'), headers=headers, method="PUT")
            try:
                with urllib.request.urlopen(put_req) as resp:
                    print(f"  [✓] {rel_path}")
            except urllib.error.HTTPError as e:
                print(f"  [✗] Error subiendo {rel_path}: {e.code}")

    # 3. Habilitar GitHub Pages
    print("[*] Configurando GitHub Pages...")
    pages_url = f"https://api.github.com/repos/{github_username}/{repo_name}/pages"
    pages_payload = {
        "build_type": "workflow"
    }
    pages_req = urllib.request.Request(pages_url, data=json.dumps(pages_payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(pages_req) as resp:
            print("[+] GitHub Pages configurado con éxito.")
    except urllib.error.HTTPError:
        pass

    static_url = f"https://{github_username}.github.io/{repo_name}/"
    print("\n" + "="*60)
    print("🎉 ¡DESPLIEGUE COMPLETADO!")
    print(f"🔗 Tu web estará disponible de forma permanente en:")
    print(f"👉 {static_url}")
    print(f"📁 Repositorio: https://github.com/{github_username}/{repo_name}")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        user = sys.argv[1]
        token = sys.argv[2]
        upload_project(user, token)
    else:
        print("Uso: python deploy_to_github.py <TU_USUARIO_GITHUB> <TU_PERSONAL_ACCESS_TOKEN>")
        print("Obtén tu token con permisos de 'repo' en: https://github.com/settings/tokens")
