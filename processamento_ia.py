from google import genai
import data_base
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def processar_com_gemini(texto_do_email):
    try:
        # Usamos o nome que funcionou no seu teste
        prompt = f"""
        Preciso pegar as informações desses emails e organizar com estas chaves: 
        quem_mandou, quando_mandou, para_quando_e, o_que_e_para_fazer, titulo_tarefa. 
        Caso não seja uma tarefa, responda somente: "não há tarefa". Os horários você deixa no formato hh:mm  dd/mm. Não se esqueça de acrescentar o horário de quando deverá entregar a tarefa, quando houver.
        Considere reuniões como tarefas e coloque a data e a hora dela
        
        Responda ESTRITAMENTE em formato JSON seguindo esta estrutura:
        {{
            "quem_mandou": "nome@email.com",
            "quando_mandou": "21/04 - 15:17",
            "para_quando_e": "19/05",
            "o_que_e_para_fazer": "Descrição resumida da tarefa aqui.",
            "titulo_tarefa": "Título curto e direto",
            "status": "backlog"
        }}

        E-mail para analisar:
        {texto_do_email}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro na IA: {e}"
    
def executar_fluxo_ia(conteudo_para_ia):

    resposta_ia = processar_com_gemini(conteudo_para_ia)
    
    print("-" * 50)
    print("RESPOSTA DA IA:", resposta_ia)
    print("-" * 50)

    if "não há tarefa" not in resposta_ia.lower():
        sucesso = data_base.salvar_tarefa(resposta_ia)
        
        if sucesso: 
            print("✅ Dados integrados ao Kanban com sucesso!")
            return True
        else:   
            print("❌ Falha ao processar o JSON da IA.")
            return False
    else:
        print("ℹ️ Email analisado: Não é uma tarefa.")
        return False