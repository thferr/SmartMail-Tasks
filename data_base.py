import json
import os


# Caminho do arquivo
DB_FILE = 'kanban.json'

def salvar_tarefa(resposta_bruta_ia):
    """
    Recebe a string JSON do Gemini, limpa as marcações de markdown,
    converte para dicionário e salva no arquivo kanban.json.
    """
    try:
        # 1. Limpeza da string (remove as crases de markdown se existirem)
        texto_limpo = resposta_bruta_ia.replace('```json', '').replace('```', '').strip()
        
        # 2. Converte a string limpa em um dicionário Python
        dados_ia = json.loads(texto_limpo)
        
        # O Gemini entrega como {"tarefa": {...}}, pegamos só o conteúdo interno
        nova_tarefa = dados_ia.get("tarefa", dados_ia)
        
        # Adicionamos um status padrão para o Kanban se não existir
        if "status" not in nova_tarefa:
            nova_tarefa["status"] = "backlog"

        # 3. Carrega a lista atual do arquivo
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                try:
                    lista_tarefas = json.load(f)
                except json.JSONDecodeError:
                    lista_tarefas = []
        else:
            lista_tarefas = []

        # 4. Adiciona a nova tarefa e salva de volta
        lista_tarefas.append(nova_tarefa)
        
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(lista_tarefas, f, indent=4, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"Erro ao salvar no JSON: {e}")
        return False