from imap_tools import MailBox, AND
import processamento_ia
import time
import os
from dotenv import load_dotenv

# CONFIGURAÇÕES DE ACESSO
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
SENHA = os.getenv("EMAIL_PASS")
INTERVALO_CHECK = 120 # Verifica a cada 2 minutos (120 segundos)

def rodar_verificacao():
    """
    Executa a rotina de busca de emails e processamento via IA.
    Utiliza a lógica de autenticação imap-tools fornecida.
    """
    try:
        with MailBox('imap.gmail.com').login(EMAIL, SENHA, initial_folder='INBOX') as mailbox:
            print(f"[{time.strftime('%H:%M:%S')}] LOGIN OK!")

            # Busca e-mails não lidos (limitado a 3)
            for msg in mailbox.fetch(AND(seen=False), limit=3, reverse=True):
                conteudo_para_ia = f""" 
                ASSUNTO: {msg.subject}
                DE: {msg.from_}
                DATA: {msg.date}
                CORPO DO TEXTO: {msg.text}
                """
                print(f"Lendo: {msg.subject}")

                # Envia o conteúdo para a função de fluxo no processamento_ia
                processamento_ia.executar_fluxo_ia(conteudo_para_ia)
                
    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    print("=== MONITORAMENTO AUTOMÁTICO INICIADO ===")
    
    # Loop infinito para execução periódica
    while True:
        rodar_verificacao()
        print(f"Aguardando {INTERVALO_CHECK/60} minutos para a próxima verificação...")
        time.sleep(INTERVALO_CHECK)

    






