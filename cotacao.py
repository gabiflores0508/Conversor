import requests


def buscar_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        return float(dados["USDBRL"]["bid"])
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Erro ao acessar API: {e}")
        return None


def converter_valor(valor_em_reais, cotacao):
    if valor_em_reais <= 0 or cotacao is None:
        return None
    return round(valor_em_reais / cotacao, 2)


try:
    cotacao_atual = buscar_cotacao()
    print(f"Cotação encontrada: {cotacao_atual}")
    if cotacao_atual:
        valor = float(input("Digite o valor em reais para converter: R$ "))
        convertido = converter_valor(valor, cotacao_atual)
        print(f"Valor em dólares: ${convertido}")
    else:
        print("Erro ao buscar a cotação do dólar.")
except ValueError:
    print("Valor inválido. Tente novamente.")
except KeyboardInterrupt:
    print("\nOperação interrompida pelo usuário.")
except Exception as e:
    print(f"Erro inesperado: {e}")
