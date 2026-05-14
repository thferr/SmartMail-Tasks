from flask import Flask, render_template, redirect, url_for, request
import json
import os

app = Flask(__name__)
DB_FILE = 'kanban.json'

def carregar_dados():
    """Lê o ficheiro JSON e garante que os dados estão numa lista limpa."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
                # Garante que é uma lista. Se for um único objeto, envolve em lista.
                if isinstance(dados, dict):
                    return [dados]
                return dados if isinstance(dados, list) else []
            except Exception as e:
                print(f"Erro ao ler JSON: {e}")
                return []
    return []

def salvar_dados(dados):
    """Guarda a lista de volta no ficheiro JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    todas_tarefas = carregar_dados()
    # Criamos um ID temporário baseado na posição real da lista para o HTML saber quem é quem
    for i, t in enumerate(todas_tarefas):
        t['id_original'] = i
    return render_template('index.html', tarefas=todas_tarefas)

@app.route('/mover/<int:indice>/<novo_status>')
def mover(indice, novo_status):
    """
    Altera o status da tarefa no JSON e recarrega a página.
    """
    dados = carregar_dados()
    if 0 <= indice < len(dados):
        # Acedemos à tarefa pelo índice absoluto enviado pelo botão
        dados[indice]['status'] = novo_status
        salvar_dados(dados)
        print(f"✅ Sucesso: Tarefa {indice} movida para {novo_status}")
    else:
        print(f"❌ Erro: Índice {indice} inválido.")
    
    # O redirect força o refresh da página
    return redirect(url_for('index'))

@app.route('/excluir/<int:indice>')
def excluir(indice):
    """
    Remove a tarefa da lista e atualiza o JSON.
    """
    dados = carregar_dados()
    if 0 <= indice < len(dados):
        dados.pop(indice)
        salvar_dados(dados)
        print(f"🗑️ Tarefa {indice} removida.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Rodar na porta 5000
    app.run(debug=True, port=5000)