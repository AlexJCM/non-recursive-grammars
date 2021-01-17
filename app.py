from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------ENDPOINTS--------------------------
@app.route('/')
def init():
    return render_template('app.html')

@app.route('/', methods=['POST'])
def convertir_rules():
    """
    Entrada esperada:
        A->A1
        A->0BC
    Salida resultante:
        A->0BCA'
        A'->1A'
        A'->λ
    """
    if request.method == 'POST':
        gramatica = request.form['reglas']  # Se obtiene del formulario html
        if gramatica == '':
            print("La gramatica está vacía")
            return render_template('app.html', gramatica=gramatica)

        # Guardamos las reglas ingresadas en un arreglo
        lista_reglas = gramatica.split('\r\n')
        # eliminar valores vacios del arreglo
        lista_reglas = [item for item in lista_reglas if item]
        resultado = generate_non_recursive_rules(lista_reglas)
        return render_template('app.html', resultado=resultado, gramatica=gramatica)
        


# ---------------------FUNCIONES--------------------------
def generate_non_recursive_rules(lista_reglas):
    resultado = []
    for i in range(0, len(lista_reglas) - 1):
        ruler = lista_reglas[i].replace(" ", "")  # eliminar espacios en blanco
        simbolo_inicial = ruler[0]

        # Obtener valores descartados solo de la primera regla
        aux = lista_reglas[0]
        descartados = aux[4:]
        print("descartados = ", descartados)

        if simbolo_inicial == ruler[3]:
            print('Es una regla recursiva')
            # Generar reglas no recursivas (reglaNR)
            # 1. En la primera reglaSR busco si el simbolo inicial está luego del ->.
            # 2. Luego genero una primera reglaNR con dicho simbolo inicial que contenga el valor de la siguiente reglaSR,
            #    despues, le agrego dicho simbolo inicial al final junto con el simbolo prima (Ejm.: A')
            #    y descarto los demas simbolos.
            # 3. Genero una segunda reglaNR, la cual empieza con el simbolo inicial pero concatenado con prima, este contiene
            #    a los simbolos descartados en el paso anterior y finaliza con el simbolo inicial concatenado con prima.
            # 4. Genero una tercera reglaNR, la cual empieza con el simbolo inicial pero concatenado con prima, este solo
            #    contiene a la cadena vacia.           
            if i == 0:
                next_ruler = lista_reglas[i + 1].replace(" ", "")
                values_next_ruler = next_ruler[3:]
                print("values_next_ruler = ", values_next_ruler)
                new_ruler = simbolo_inicial + "->" + values_next_ruler + simbolo_inicial + "'"
                print("reglaNR 1 = ", new_ruler)
                resultado.append(new_ruler)
            
            new_ruler = simbolo_inicial + "'" + "->" + descartados + simbolo_inicial + "'"
            print("reglaNR 2 = ", new_ruler)
            resultado.append(new_ruler)


    # Generarmos la última regla que contiene la cadena vacia     
    new_ruler = simbolo_inicial + "'" + "->" + 'λ'
    resultado.append(new_ruler)
    print(resultado)

    return resultado


# --------------------------------------------------------
if __name__ == ' __main__':
    app.debug = True
    app.run()
