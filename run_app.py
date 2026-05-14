import threading
import time
import sys
import os

# Importamos as funções dos seus ficheiros originais
# Certifique-se de que os nomes dos ficheiros (app.py e main.py) estão correctos na mesma pasta
try:
    from app import app as flask_app
    import main as email_monitor
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("Certifique-se de que os ficheiros app.py e main.py estão na mesma directoria.")
    sys.exit(1)

def rodar_servidor_web():
    """Executa o servidor Flask em modo de produção."""
    print("🌐 [Sistema] Iniciando interface web em http://127.0.0.1:5000")
    flask_app.run(debug=False, port=5000, use_reloader=False)

def rodar_monitor_email():
    """Executa o loop de monitorização de e-mails do main.py."""
    print("📧 [Sistema] Iniciando serviço de monitorização de e-mails...")
    while True:
        try:
            email_monitor.rodar_verificacao()
        except Exception as e:
            print(f"⚠️ [Erro Email] Falha na ronda de verificação: {e}")
        
        # Espera 5 minutos para a próxima verificação (300 segundos)
        time.sleep(300)

if __name__ == "__main__":
    print("="*50)
    print("   SISTEMA DE KANBAN COM IA - INICIANDO COMPONENTES")
    print("="*50)

    # 1. Criamos as threads para os dois processos rodarem em paralelo
    thread_web = threading.Thread(target=rodar_servidor_web)
    thread_email = threading.Thread(target=rodar_monitor_email)

    # 2. Definimos como daemon para que as threads morram quando o programa principal fechar
    thread_web.daemon = True
    thread_email.daemon = True

    # 3. Iniciamos ambos os motores
    thread_web.start()
    thread_email.start()

    print("\n🚀 Tudo pronto! Pode minimizar esta janela.")
    print("Pressione Ctrl+C neste terminal para encerrar o sistema completo.\n")

    # Mantém o script pai vivo enquanto as tarefas de fundo trabalham
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando serviços de forma segura...")
        sys.exit(0)