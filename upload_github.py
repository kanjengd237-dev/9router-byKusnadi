import os
import subprocess
import requests

# =========================================================
# KONFIGURASI (Isi data Anda di sini)
# =========================================================
GITHUB_TOKEN = "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"  # Masukkan Personal Access Token Anda
REPO_NAME = "9router-byKusnadi"                         # Nama repo yang ingin dibuat
IS_PRIVATE = False                                          # True jika ingin repo Privat, False jika Publik
FOLDER_PATH = "."                                           # Path folder yang ingin diupload ("." untuk folder saat ini)
# =========================================================


def create_github_repo(token, repo_name, private=False):
    """Membuat repository baru di GitHub via REST API."""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": repo_name,
        "private": private,
        "auto_init": False
    }

    print(f"[*] Membuat repository '{repo_name}' di GitHub...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        repo_data = response.json()
        print(f"[✓] Repository berhasil dibuat: {repo_data['html_url']}")
        return repo_data['clone_url']
    elif response.status_code == 422:
        print(f"[!] Repository '{repo_name}' sudah ada di akun Anda.")
        user_res = requests.get("https://api.github.com/user", headers=headers).json()
        username = user_res['login']
        return f"https://github.com/{username}/{repo_name}.git"
    else:
        print(f"[X] Gagal membuat repository: {response.status_code}")
        print(response.json())
        return None

def run_cmd(command, cwd=None):
    """Menjalankan perintah terminal/bash."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
    if result.returncode != 0:
        print(f"[X] Error menjalankan: {command}")
        print(result.stderr)
        return False
    return True

def upload_to_github(token, clone_url, folder_path):
    """Melakukan inisialisasi git, commit, dan push ke GitHub."""
    os.chdir(folder_path)

    # Format URL remote menggunakan token agar tidak perlu input password manual
    auth_url = clone_url.replace("https://", f"https://{token}@")

    print("[*] Menginisialisasi Git lokal dan mengunggah file...")

    # Jalankan perintah Git berurutan
    if not os.path.exists(".git"):
        run_cmd("git init")
    
    run_cmd("git branch -M main")
    run_cmd("git add .")
    run_cmd('git commit -m "Auto commit & upload via Python script"')
    
    # Hapus origin lama jika ada, lalu tambahkan origin baru
    run_cmd("git remote remove origin")
    run_cmd(f"git remote add origin {auth_url}")
    
    # Push ke GitHub
    if run_cmd("git push -u origin main"):
        print("[✓] SEMUA FILE BERHASIL DIUPLOAD KE GITHUB!")
    else:
        print("[X] Gagal mengunggah file ke GitHub.")

if __name__ == "__main__":
    if GITHUB_TOKEN == "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX":
        print("[!] Harap isi GITHUB_TOKEN Anda terlebih dahulu di dalam script.")
    else:
        remote_url = create_github_repo(GITHUB_TOKEN, REPO_NAME, IS_PRIVATE)
        if remote_url:
            upload_to_github(GITHUB_TOKEN, remote_url, FOLDER_PATH)
