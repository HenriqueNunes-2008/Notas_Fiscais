from flask import Flask, render_template, request, jsonify, send_file
import psycopg2
import os
import pandas as pd # Importante: adicione pandas
import io

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL') 

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# --- NOVA ROTA PARA O EXCEL ---
@app.route('/baixar-dados')
def baixar_dados():
    try:
        conn = get_db_connection()
        # Lê a tabela do banco de dados direto para um DataFrame do Pandas
        query = "SELECT data, n_nota, fornecedor, material, unidade, quantidade, valor_unitario, valor_total, projeto FROM notas"
        df = pd.read_sql(query, conn)
        conn.close()

        # Prepara o arquivo CSV na memória
        output = io.StringIO()
        # Usamos sep=';' e decimal=',' para o Excel abrir direto sem precisar configurar nada
        df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
        
        # Converte para bytes para o Flask enviar
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8-sig'))
        mem.seek(0)

        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name='dados_sistema.csv'
        )
    except Exception as e:
        return f"Erro ao gerar CSV: {str(e)}"

@app.route('/adicionar', methods=['POST'])
def adicionar():
    try:
        data_nota = request.form.get('data')
        n_nota = request.form.get('n_nota')
        fornecedor = request.form.get('fornecedor')
        materiais = request.form.getlist('material[]')
        quantidades = request.form.getlist('quantidade[]')
        valores_unit = request.form.getlist('valor_unitario[]')
        unidades = request.form.getlist('unidade[]')
        projetos = request.form.getlist('projeto[]')

        if not materiais:
            return jsonify({"status": "error", "message": "Nenhum material informado."})

        conn = get_db_connection()
        cur = conn.cursor()

        for i in range(len(materiais)):
            qtd = float(quantidades[i] or 0)
            v_unit = float(valores_unit[i] or 0)
            v_total = qtd * v_unit
            
            cur.execute("""
                INSERT INTO notas (data, n_nota, fornecedor, material, unidade, quantidade, valor_unitario, valor_total, projeto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data_nota, n_nota, fornecedor, materiais[i], unidades[i], qtd, v_unit, v_total, projetos[i]))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success", 
            "message": f"✅ {len(materiais)} itens salvos com sucesso!"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Erro ao salvar: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
