def TransformaTexto(texto):
    texto = texto.replace('R$', '')
    texto = texto.replace('.', '')
    texto = texto.replace(',', '.')
    
    return float(texto)