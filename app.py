from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

import os

# URL sheets
GOOGLE_SCRIPT_URL = os.environ.get('GOOGLE_SCRIPT_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    try:
        # 1. Coleta os dados básicos do formulário
        data_nota = request.form.get('data')
        n_nota = request.form.get('n_nota')
        fornecedor = request.form.get('fornecedor')
        
        # 2. Coleta as listas de materiais
        materiais = request.form.getlist('material[]')
        unidades = request.form.getlist('unidade[]')
        quantidades = request.form.getlist('quantidade[]')
        valores_unit = request.form.getlist('valor_unitario[]')
        projetos = request.form.getlist('projeto[]')

        if not materiais:
            return jsonify({"status": "error", "message": "Nenhum material informado."})

        # 3. Monta o pacote de dados para o Google Sheets
        pacote_dados = {
            "data_nota": data_nota,
            "n_nota": n_nota,
            "fornecedor": fornecedor,
            "itens": []
        }

        for i in range(len(materiais)):
            qtd = float(quantidades[i] or 0)
            v_unit = float(valores_unit[i] or 0)
            pacote_dados["itens"].append({
                "material": materiais[i],
                "unidade": unidades[i],
                "quantidade": qtd,
                "valor_unitario": v_unit,
                "valor_total": qtd * v_unit,
                "projeto": projetos[i]
            })

        # 4. Envia os dados para o Google Apps Script via POST
        response = requests.post(GOOGLE_SCRIPT_URL, json=pacote_dados)
        
        if response.status_code == 200:
            return jsonify({
                "status": "success", 
                "message": f"✅ {len(materiais)} itens enviados direto para o Google Sheets!"
            })
        else:
            return jsonify({"status": "error", "message": "Erro na comunicação com o Google."})

    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Erro ao processar: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
