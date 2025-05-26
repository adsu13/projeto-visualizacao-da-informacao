import os
import subprocess
import time
SCRIPTS = [
    "./src/plot1.py",
    "./src/plot2.py",
    "./src/plot3.py",
    "./src/dashboard.py"
]
def run_scripts():
    print("Iniciando geração de gráficos...\n")
    for script in SCRIPTS:
        script_name = script.replace(".py", "")
        
        try:
            print(f"Gerando {script_name}...", end=" ", flush=True)
            subprocess.run(["python", script], check=True)
            print(f"Gráfico {script_name} gerado com sucesso! ✅")
            time.sleep(1)
        except subprocess.CalledProcessError:
            print(f"Falha ao gerar {script_name} ❌")
            break 
        except FileNotFoundError:
            print(f"Arquivo {script} não encontrado ❌")
            break
    print("\nProcesso concluído!")
if __name__ == "__main__":
    run_scripts()