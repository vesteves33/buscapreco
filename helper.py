import yagmail as yg



def TransformaTexto(texto):
    texto = texto.strip()
    texto = texto.replace('R$', '')
    texto = texto.replace('.', '')
    texto = texto.replace(',', '.')
    
    return float(texto)
  
def EnviaEmail(desconto, produtos, receptor='vesteves33@gmail.com'):
    user = 'vesteves33@gmail.com'
    password = '300694vitoR.'
    
    email = yg.SMTP(user=user, password=password)

    receiver = receptor
    subject = f'Alerta de preço dos produtos com desconto de {desconto:.0%}'  
    contents = f'<p>Estes são os produtos com de {desconto:.0%} desconto</p>{produtos}'

    return email.send(receiver, subject, contents) 