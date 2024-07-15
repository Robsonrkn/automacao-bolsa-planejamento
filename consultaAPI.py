import requests
import json
import csv
from datetime import date

data_hoje = date.today()
data_hoje = data_hoje.strftime("%d_%m_%Y")
i = 1
j = 1
cabecalho_feito = True

with open (".\\FonteDeDados\\fields.txt","r") as f:
    itens_para_coletar = csv.reader(f, delimiter=";")
    dados_itens_para_coletar = list(itens_para_coletar)
with open(".\\FonteDeDados\\DadosBase\\Papel_Valor.csv", "r") as file:
    csv_papeis = csv.reader(file, delimiter=";")

    for row in csv_papeis:
        print(row[0])

        response = requests.get(f"https://brapi.dev/api/quote/{row[0]}?token=nsWXbLAzMqLcGXduC1mmKe")
        dados = response.json()

        try:
            if response.status_code == 200:
                print("Consulta realizada com sucesso")
            else:
                print("Consulta não realizada, erro status code: " + str(response.status_cod))
        except requests.exceptions.RequestException as e:
            print(f'Erro na requisição: {e}')

        with open(f".\\Resultado\\dadosDosAivosDaCarteira.csv", "a") as file:
            for item in dados['results']:
                linha_new_csv = ""
                cabecalho_csv = ""

                for chave, valor in item.items():
                    for metrica in dados_itens_para_coletar:
                        rMetrica = str(metrica).replace("'", "").replace("[","").replace("]","")
                        if str(chave).__contains__(str(rMetrica)):
                            cabecalho_csv += str(chave)
                            cabecalho_csv += ";"
                            #if str(chave) == "regularMarketTime":
                            #    cabecalho_csv += "Data da extração; Hora da extração;"
                    if cabecalho_feito == False and i >= len(item):
                            cabecalho_csv = cabecalho_csv[:-1]
                            cabecalho_csv += '\n'
                            file.write(str(cabecalho_csv))
                            cabecalho_feito = True
                    else:
                        i += 1
                for chave, valor in item.items():
                    for metrica in dados_itens_para_coletar:
                        rMetrica = str(metrica).replace("'", "").replace("[","").replace("]","")
                        if str(chave).__contains__(str(rMetrica)):
                            if str(valor).__contains__(".") :
                                linha_new_csv += str(valor).replace(".", ",")
                                linha_new_csv += str(";")
                            else:
                                linha_new_csv += str(valor)
                                linha_new_csv += str(";")
                            #if str(chave) == "regularMarketTime":
                            #    linha_new_csv += ";"
                            #    linha_new_csv += str(valor).split("T")[0]
                            #    linha_new_csv += ";"
                            #    linha_new_csv += str(valor).split("T")[1].split(".")[0]
                    if j >= len(item):
                        linha_new_csv = linha_new_csv[:-1]
                        linha_new_csv += '\n'
                        file.writelines(str(linha_new_csv))
                        j = 1
                    else:
                        j += 1
                print(linha_new_csv)
