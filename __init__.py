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
    
    
    
    try:
        #percorendo Amazon
        driver.get(linha['Amazon'])
        precoAmazon = driver.find_element_by_id('priceblock_ourprice').text

        #percorrendo Lojas Americanas
        driver.get(linha['Lojas Americanas'])
        precoAmericanas = driver.find_element_by_class_name('src__BestPrice-sc-1jvw02c-5').text
        
        #percorrendo Magazine Luiza
        driver.get(linha['Magazine Luiza'])
        precoMagalu = driver.find_element_by_class_name('price-template__text').text    
        
    except:
        driver.get(linha['Amazon'])
        precoAmazon = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[5]/div[3]/div[4]/div[8]/div[1]/div/table/tbody/tr[1]/td[2]/span[1]').text
        
        driver.get(linha['Lojas Americanas'])
        precoAmericanas = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div').text
    
        driver.get(linha['Magazine Luiza'])
        precoMagalu = ''
       
    precoAmazon = TransformaTexto(precoAmazon)
    precoAmericanas = TransformaTexto(precoAmericanas)
    precoMagalu = TransformaTexto(precoMagalu)    
    
    print(precoAmazon, precoAmericanas, precoMagalu)
    
    listaPrecos = [(precoAmazon, 'Amazon'), (precoAmericanas, 'Americanas'), (precoMagalu, 'Magalu'), (precOriginal, 'Original')]
    #Ao utilizar o metodo sort irá organizar a partir do primeiro item de cada Tupla, nesse caso os preços
    listaPrecos.sort()
    
    
    #preenchendo a planilha com o menor valor
    produtos.loc[i, 'Preço Atual'] = listaPrecos[0][0]
    produtos.loc[i, 'Local'] = listaPrecos[0][1]

#salvando o arquivo em excel    
produtos.to_excel('/home/vitor/Projetos/Python/buscapreco/storage/Produtos.xlsx')

descontoMinimo = 0.2

#usará todas as colunas
tabelaFiltrada = produtos.loc[produtos['Preço Atual'] <= produtos['Preço Original']*(1-descontoMinimo), :]
user = 'vesteves33@gmail.com'
password = '300694vitoR.'

receiver = user
subject = 'Alerta de preço dos produtos com desconto'  
contents = f'''
<p>Estes são os produtos com de {descontoMinimo:.0%}% desconto</p>
<p>{tabelaFiltrada.to_html()} </p>
'''



email = yg.SMTP(user, password)

email.send(receiver, subject, contents)
        