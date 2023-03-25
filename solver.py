##########################Giovany da Silva Santos######################################
#Testing
#Função util para ordenar a lista de acordo com o 3º elemento dos blocos analisados
def takeThird(elem):
    return elem[2]
    
#Função que recebe um valor e verifica se ele é um número inteiro ou não      
def isInt(value):
  try:
    int(value)
    return True
  except:
    return False

#Função que recebe um dado e verifica se o campo SIDE_TYPE é igual a BUY ou SELL 
def valida_side_type(dado):
    return dado.split(":")[1] == "BUY" or dado.split(":")[1] == "SELL" 

#Função que recebe um dado e verifica se o campo QTY é inteiro
#Caso seja inteiro, é verificado se é positivo e múltiplo de 10 
def valida_qty(dado):
    if(isInt(dado.split(":")[1]) == False):
	    return False
    return  int(dado.split(":")[1])>0 and int(dado.split(":")[1])% 10 == 0

#Função que recebe um dado e verifica se o campo TICKER contém entre 5 e 6 letras, 
#tbm se o campo iniciacom 4 letras e se os últimos dígitos é um inteiro
def valida_ticker(dado):
	palavra = dado.split(":")[1]
	return len(palavra)>=5 and len(palavra)<=6 and palavra[0:4].isalpha() and isInt(palavra.replace(palavra[0:4],"")) 



    
def main():
#abertura do arquivo com nome gotham_op.txt     
    arquivo = open("gotham_op.txt","r")

#armazenamento das linhas em uma variavel    
    linhas = arquivo.readlines()

#Declaração de variáveis que serão utilizadas
    lista_ticker = []#Armazena todos dados agrupados por ticker
    lista_tickers_diferentes = []#Armazena os tipos de tickers diferentes
    lista_resultante = []#Armazena o valor calculado por ticker
    total_linhas = len(linhas)#Armazena a quantidade linhas
    linhas_invalidas = []#Lista booleana para identificar se uma linha i é inválida
    
#Seta como false a invalidade de todas linhas
    linhas_invalidas = [False for i in range(total_linhas)]
    
#cada linha será processada:
    for i in range(total_linhas):
	    linha_split = linhas[i].split(";")#Separa os dados da linha por ;
        
#Cria uma estrutura auxiliar para armazenar os dados separadamente para dpois ser adicionado na lista
	    dado = []
	    dado.append(linha_split[0])
	    dado.append(linha_split[1])
	    dado.append(linha_split[2].replace("\n",""))
	    dado.append(i)

#Adciona o tipo de ticker na lista de diferentes 
	    lista_tickers_diferentes.append(linha_split[2].replace("\n",""))

#Se o dado é Inválido marque como inválido	    
	    if(valida_side_type(dado[0]) == False or valida_qty(dado[1]) == False or valida_ticker(dado[2]) == False ):
	        linhas_invalidas[i] = True
	    lista_ticker.append(dado)#Adiciona o dado na lista de tickers

#Ordena a lista pelo ticker
    lista_ticker.sort(key = takeThird)
#Cria uma lista auxiliar para agrupar por ticker 
    lista_agrupada = []

#Elimina elementos repetidos da lista    
    lista_tickers_diferentes = set(lista_tickers_diferentes)

#Para cada ticker se for válido adciona na lista agrupada   
    for tipo_ticker in lista_tickers_diferentes:
        res=[(side_type,qty,ticker,pos) for (side_type,qty,ticker,pos) in lista_ticker if ticker == tipo_ticker and linhas_invalidas[pos] == False]
        if res != []:
            lista_agrupada.append(res)
    
#Para cada grupo na lista agrupada calcule o valor final de QTY           
    for grupo in lista_agrupada:
        valor = 0 #var auxiliar setada como zero
        ticker = grupo[0][2].split(":")[1]#retorna 3º elemento(ticker)
        
        for dado in grupo:
            side_type = dado[0].split(":")[1]#retorna 1º elemento(side_type)
            qty = dado[1].split(":")[1]#retorna 2º elemento(qty)
 
#soma ou subtrai de acordo com a operação            
            if(side_type == "SELL"):
                valor -= int(qty)
            else:
                valor += int(qty)
                
#adiciona a lista resultante o valor referente àquele ticker
        lista_resultante.append([ticker,valor])

#Ordena a lista(por padrão ocorre pelo 1º elemento ou seja ticker)
    lista_resultante.sort()

#Print da linhas válidas
    print("Total que foi comprado e vendido no dia por ativo")
    for dado in lista_resultante:
        print(dado[0] +": " +str(dado[1]))
    print()

#Print da linhas válidas
    print("Linhas inválidas:")

#Variável utilizada para verificar se existe pelo menos uma linha inválida
    existe_invalida = False

    for i in range(total_linhas):
        if(linhas_invalidas[i] == True):
            existe_invalida = True#Existe alguma linha inválida
            string =""#String que será utilizada para o print 

#Busca por linhas inválidas            
            dado = []
            dado = [(side_type,qty,ticker,pos) for (side_type,qty,ticker,pos) in lista_ticker if pos == i]

#Verifica o tipo de invalidez da linha            
            if(valida_side_type(dado[0][0]) == False):
                string += "Valor Inválido de SIDE;"
            
            if(valida_qty(dado[0][1]) == False):
                if(isInt(dado[0][1].split(":")[1]) == False):
                    string += "Valor Inválido de QTY;"
                
                else:
                    if(int(dado[0][1].split(":")[1]) <=0):
                        string += "QTY não é positivo;"
                    
                    if(int(dado[0][1].split(":")[1]) % 10 != 0):
                        string += "QTY não é múltiplo de 10;"
                    
            if(valida_ticker(dado[0][2]) == False):
                string += "TICKER mal formatado;"
            print(str(linhas[i])+string+"\n")
 
#Caso não exista pelo menos uma linha inválida então imprime Nenhuma       
    if(existe_invalida == False):
        print("Nenhuma")
            
if __name__ == '__main__':
    main()
