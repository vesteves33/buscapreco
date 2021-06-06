from helper import TransformaTexto, EnviaEmail, VerificaDF
import pandas as pd
from selenium import webdriver
from xvfbwrapper import Xvfb
import time

#importação da base pra dentro do script
produtos = pd.read_excel('/home/vitor/Projetos/Python/buscapreco/storage/Produtos.xlsx')
produtos = produtos.fillna('-')

#lib para ocultar navegador durante execução do código
display = Xvfb()
display.start()

#inserindo o driver pra utilização do Selenium
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
#driver.set_window_position(-10000, 0)

#percorrendo os dados contidos no dataframe produtos
for i, linha in produtos.iterrows():
    nomeProduto = linha['Link Produto']
    precOriginal = linha['Preço Original']
    
    
    #Bloco percorrendo Amazon
    driver.get(linha['Amazon'])
    try:
        #percorendo Amazon
        precoAmazon = driver.find_element_by_id('priceblock_ourprice').text
        precoAmazon = TransformaTexto(precoAmazon)

    except:
        try:   
            #utilizar elemento alternativo ao id dentr da pagina
            precoAmazon = driver.find_element_by_id('priceblock_ourprice').text
            precoAmazon = TransformaTexto(precoAmazon)
        except:
            print(f'Produto {linha["Link Produto"]} indisponível no link da Amazon')
            precoAmazon = linha['Preço Original'] * 3
    
    #Bloco Americanas
    driver.get(linha['Lojas Americanas'])
    try:    
        #percorrendo Lojas Americanas
        precoAmericanas = driver.find_element_by_class_name('src__BestPrice-sc-1jvw02c-5').text
        precoAmericanas = TransformaTexto(precoAmericanas)
    except:
        try:
            #utilizar elemento alternativo na pagina do produto
            precoAmericanas = driver.find_element_by_class_name('src__BestPrice-sc-1jvw02c-5').text        
            precoAmericanas = TransformaTexto(precoAmericanas)
        except:
            print(f'Produto {linha["Link Produto"]} indisponível no link das Americanas')
            precoAmericanas = linha['Preço Original'] * 3 
    
    #Bloco Magazine Luiza
    driver.get(linha['Magazine Luiza'])
    try:
        #percorrendo Magazine Luiza
        precoMagalu = driver.find_element_by_class_name('price-template__text').text    
        precoMagalu = TransformaTexto(precoMagalu)
    except:    
        try:
            #utilizar elemento alternativo na pagina do produto
            precoMagalu = driver.find_element_by_class_name('price-template__text').text
            precoMagalu = TransformaTexto(precoMagalu)
        except:    
            print(f'Produto {linha["Link Produto"]} indisponível no link das Americanas')
            precoMagalu = linha['Preço Original'] * 3  
    
    
    listaPrecos = [(precoAmazon, 'Amazon'), (precoAmericanas, 'Americanas'), (precoMagalu, 'Magalu'), (precOriginal, 'Original')]
    #Ao utilizar o metodo sort irá organizar a partir do primeiro item de cada Tupla, nesse caso os preços
    listaPrecos.sort()
    
    
    #preenchendo a planilha com o menor valor
    produtos.loc[i, 'Preço Atual'] = listaPrecos[0][0]
    produtos.loc[i, 'Local'] = listaPrecos[0][1]

#salvando o arquivo em excel    
produtos.to_excel('/home/vitor/Projetos/Python/buscapreco/storage/Produtos.xlsx')

driver.quit()
display.stop()  


descontoMinimo = 0.2

#usará todas as colunas
tabelaFiltrada = produtos.loc[produtos['Preço Atual'] <= produtos['Preço Original']*(1-descontoMinimo), :]
tabelaFiltrada = VerificaDF(tabelaFiltrada)
tabelaFiltrada = tabelaFiltrada.to_html()


if True:
    EnviaEmail(descontoMinimo, tabelaFiltrada)
print('Sucesso')
        
#função que mantem programa aguardando tempo para executar novamente
time.sleep(3600*5)