from helper import TransformaTexto
import pandas as pd
import yagmail as yg
from selenium import webdriver

#importação da base pra dentro do script
produtos = pd.read_excel('/home/vitor/Projetos/Python/buscapreco/storage/Produtos.xlsx')
produtos = produtos.fillna('-')



#inserindo o driver pra utilização do Selenium
#driver = webdriver.Chrome()
driver = webdriver.Firefox()

#percorrendo os dados contidos no dataframe produtos
for i, linha in produtos.iterrows():
    nomeProduto = linha['Link Produto']
    precOriginal = linha['Preço Original']
    
    
    #percorendo Amazon
    driver.get(linha['Amazon'])
    precoAmazon = driver.find_element_by_id('priceblock_ourprice').text
    #removendo R$ da variavel
    precoAmazon = TransformaTexto(precoAmazon)


    #percorrendo Lojas Americanas
    driver.get(linha['Lojas Americanas'])
    precoAmericanas = driver.find_element_by_class_name('src__BestPrice-sc-1jvw02c-5').text
    #tratamento do texto
    precoAmericanas = TransformaTexto(precoAmericanas)

    
    #percorrendo Magazine Luiza
    driver.get(linha['Magazine Luiza'])
    precoMagalu = driver.find_element_by_class_name('price-template__text').text
    precoMagalu = TransformaTexto(precoMagalu)

    listaPrecos = [(precoAmazon, 'Amazon'), (precoAmericanas, 'Americanas'), (precoMagalu, 'Magalu'), (precOriginal, 'Original')]
    #Ao utilizar o metodo sort irá organizar a partir do primeiro item de cada Tupla, nesse caso os preços
    listaPrecos.sort()
    
    
    #preenchendo a planilha com o menor valor
    produtos.loc[i, 'Preço Atual'] = listaPrecos[0][0]
    produtos.loc[i, 'Local'] = listaPrecos[0][1]

#salvando o arquivo em excel    
produtos.to_excel('/home/vitor/Projetos/Python/buscapreco/storage/Produtos.xlsx')