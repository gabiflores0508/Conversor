from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)


def buscar_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    try:
        # Realizando a requisição para pegar os dados
        resposta = requests.get(url)
        resposta.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Processa a resposta em formato JSON
        dados = resposta.json()

        # A cotação do dólar está dentro da chave 'USDBRL' e o valor de 'bid'
        cotacao = dados["USDBRL"]["bid"]

        return float(cotacao)  # Retorna a cotação convertida para float

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Erro ao acessar a API: {e}")
        return None


@app.route("/")
def index():
    cotacao = buscar_cotacao()
    return render_template("index.html", cotacao=cotacao)


@app.route("/converter", methods=["POST"])
def converter():
    valor_em_reais = float(request.form["valor"])
    cotacao_atual = buscar_cotacao()
    if cotacao_atual and valor_em_reais > 0:
        valor_convertido = round(valor_em_reais / cotacao_atual, 2)
        return jsonify({"valor_convertido": valor_convertido})
    return jsonify({"error": "Valor inválido ou cotação indisponível"})


if __name__ == "__main__":
    app.run(debug=True)
