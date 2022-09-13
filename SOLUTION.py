import os
from bs4 import BeautifulSoup
import pandas as pd
#LINK para acesso ao código no colab https://colab.research.google.com/drive/10UudTI-KbzJVXCtOiHXV1vOlcY1_5geU?usp=sharing

#Criação de listas para armazenar os valores recebidos e gerar um dateframe final
cpf_cnpj = []
file_name = []
result = []
request_number = []
deposit_date = []
title = []
ipc = []

#Função que é chamada quando existe registros dentro da patente
def table_true(soup, path):
    #a variavel table irá procurar pelo atributo tbody dentro do HTML cujo o id seja igual á tituloContext com isso teremos acesso a os atributos
    #td onde que ficá armazenado os valores que queremos
    table = soup.find('tbody', attrs={'id': 'tituloContext'}).find_all('td')

    #Esse looping pega a quantidade de linhas que à na tabela, ou seja, se o len retornar 7 sabemos que ele terá 2 linhas,
    #isso por conta de que são 4 valores (Número do pedido, Data do deposito, Titulo, IPC), cada td representa 1 deles,
    #sendo assim; [0] representa o número do pedido, [1] representa a data do deposito, [2] representa o titulo e o [3] representa o IPC,
    #compreendemos que quando ele tem mais de uma linha ao chegar ao número [4] retornará para o número do pedido
    #e [5] para a data do deposito e assim consecutivamente. Consideramos que temos 4 números importantes, o looping andará de 4 em 4
    #por conta de que a diferença entre um valor e outro é de 1, 2 e 3, desta forma a cada vez que seu ciclo reiniciar a
    #lista pegará um atributo diferente
    for i in range(0, len(table), 4):
        #é utilizado a função .strip() para tirar os comandos \n\t que acabam ficando quando extraimos os valores
        request_number.append(table[i].find('a').text.strip())
        deposit_date.append(table[i + 1].text.strip())
        title.append(table[i + 2].text.strip())
        ipc.append(table[i + 3].text.strip())
        file_name.append(path.split('\\')[1].split('.')[0])
        cpf_cnpj.append(soup.find('div', attrs={'id': 'tituloEResumoContext'}).find('font', attrs={'class': 'normal'}).text.split("'")[1])
        result.append(soup.find('div', attrs={'id': 'tituloEResumoContextGlobal'}).find_all('font')[1].find('b').text)

#Função que é chamada quando não existe tabela dentro da patente
def table_false(soup, path):
    file_name.append(path.split('\\')[1].split('.')[0])
    cpf_cnpj.append(soup.find_all('table')[1].find_all('td')[5].find('div', attrs={'align': 'left'}).text.split("'")[1])
    result.append('0')
    request_number.append('0')
    deposit_date.append('0')
    title.append('-')
    ipc.append('-')


#list comprehension criado para entrar na pasta PATENTES e extrair o caminho completo de cada arquivo dentro dessa pasta
paths = [os.path.join('PATENTES', f) for f in os.listdir('PATENTES')]
for path in paths:
    arquivo = open(path, 'r', encoding="ISO-8859-1").read()
    soup = BeautifulSoup(arquivo, 'html5lib')
    #esse if é onde faz a verificação se existe resultado ou não, isso é possivel através de um padrão que quando existe
    #tabela existe uma div com id tituloEResumoContext
    if soup.find('div', attrs={'id': 'tituloEResumoContext'}):
        table_true(soup, path)
    else:
        table_false(soup, path)

#esse df é onde eu crio meu DataFrame com todos os resultados que eu obtive acima
df = pd.DataFrame(data={'Arquivo': file_name, 'CPF OU CNPJ': cpf_cnpj, 'Resultado': result, 'Número do pedido': request_number,
     'Data do Depósito': deposit_date, 'Título': title, 'IPC': ipc})

#Converto o meu DataFrame para uma tabela
table_patentes = df.to_html(classes='table table-stripped')

#Crio meu código em html para exibir minha tabela
codigo_html = f'''
<html>
    <head>
        <title>Patentes</title>
    </head>
    <body>
        <center>
	        {table_patentes}
        </center>
    </body>
</html>
'''

# abre o arquivo HTML para escrita
arq_html = open('PATENTES.html', 'w')

# escrevendo no arquivo HTML
arq_html.write(codigo_html)

# fechando os arquivos
arq_html.close()
