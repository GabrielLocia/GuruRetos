from flask import Flask, jsonify, request, render_template
import pymysql.cursors
import re

app = Flask(__name__)
cont = [0,0];


def hasMutation(dna):

    columna=[]
    cout_mutations = 0;
    cout_no_mutations = 6;  
    for secuencia in dna:

        #verifica mediante expresion regular si se encuentra una secuencia 
        #de cuatro letras iguales asociadas a la mutacion, la verificación 
        # es de forma horizontal dentro de la matriz.
        if re.search("A{4}",secuencia) is not None:
            print(re.search("A{4}",secuencia))
            cout_mutations = cout_mutations + 1 

        elif re.search("T{4}",secuencia) is not None:
            print(re.search("T{4}",secuencia))
            cout_mutations = cout_mutations + 1 

        elif re.search("G{4}",secuencia) is not None:
            print(re.search("G{4}",secuencia))
            cout_mutations = cout_mutations + 1 

        elif re.search("C{4}",secuencia) is not None:
            print(re.search("C{4}",secuencia))
            cout_mutations = cout_mutations + 1 
            

    #verifica mediante expresion regular si se encuentra una secuencia 
    #de cuatro letras iguales asociadas a la mutacion, la verificación 
    # es de forma vertical dentro de la matriz. 
    
    for i in range(0,6):
        columna = [fila[i] for fila in dna]  
        StrColumnas = "".join(columna)

        if re.search("A{4}",StrColumnas) is not None:
            print(StrColumnas)
            cout_mutations = cout_mutations + 1 

        elif re.search("T{4}",StrColumnas) is not None:
            print(StrColumnas)
            cout_mutations = cout_mutations + 1 

        elif re.search("G{4}",StrColumnas) is not None:
            print(StrColumnas)
            cout_mutations = cout_mutations + 1 

        elif re.search("C{4}",StrColumnas) is not None:
            print(re.search("C{4}",secuencia))
            print('Entra')
            print(StrColumnas)
            cout_mutations = cout_mutations + 1 

    if cout_mutations >= 2:
        cout_no_mutations = cout_no_mutations - cout_mutations
        return True, cout_mutations, cout_no_mutations
    else:
        return False,0,6

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/mutation', methods=['POST','GET'])
def mutacion():
    
    if request.method == 'POST':
        #Conexion a la base de datos 
        connection  = pymysql.connect(user='locia@mutationserver',
                        password='Gal14695238',
                        database='mutations',
                        host='mutationserver.mysql.database.azure.com',
                        cursorclass=pymysql.cursors.DictCursor,
                        ssl= {'ca':'./BaltimoreCyberTrustRoot.crt.pem'})

        
        dn = request.json['dna'] #obtiene el archivo json de la url 
        #comprueba si el adn tiene mutaciones
        mutations, cout_mutations, cout_no_mutations = hasMutation(dn)

        cont[0] = cont[0] + cout_mutations #posicion 0 para mutaciones
        cont[1] = cont[1] + cout_no_mutations #posicion 1 para no mutaciones

        Stradn = "".join(dn)    
    

        if mutations:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO adn(id,DNA,Mutation) VALUES(%s,%s,%s)',(0,Stradn,cout_mutations))
                connection.commit()
            return 'Se han encontrado mutaciones', 200, {'Content-Type':'text/plain'}
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO adn(id,DNA,Mutation) VALUES(%s,%s,%s)',(0,Stradn,cout_mutations))
                connection.commit()
            return 'No se encotraron mutacinones', 403, {'Content-Type':'text/plain'}
    else:
        return render_template('secueciaMutacion.html')
   

@app.route('/status')
def status():

    ratio = 0.0
    if cont[1] != 0:
        ratio = float(cont[0])/float(cont[1])
    
    Status = [
       {"count_mutation":cont[0],
        "count_no_mutation":cont[1],
        "ratio": ratio
       } 
    ]
    return  jsonify(Status)


if __name__ == '__main__':
    app.run()