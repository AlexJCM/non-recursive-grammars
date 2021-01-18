from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------ENDPOINTS--------------------------
@app.route('/', methods=['GET', 'POST'])
def convert_rules():
    error = None
    if request.method == 'POST':        
        data_string = request.form['reglas'] # Obtener los datos desde el formulario html
        gramatica = data_string.strip() # Eliminar espacios vacos del principio y final de la cadena

        if gramatica == '':
            error = ["La gramática está vacía"]
            print(error)
            return render_template('app.html', resultado=error)

        lista_reglas = gramatica.split('\r\n') # Guardamos las reglas en un arreglo
        print("lista_reglas", lista_reglas)
        lista_reglas = [item for item in lista_reglas if item] # Eliminar valores vacíos del arreglo
         
        if len(lista_reglas) < 2:
            error = ['La gramática debe tener dos reglas']
            print(error)
            return render_template('app.html', resultado=error)

        resultado = generate_non_recursive_rules(lista_reglas)
        return render_template('app.html', resultado=resultado, gramatica=gramatica)
    else:
        return render_template('app.html')


@app.errorhandler(404)
def page_not_found(error):
    return "Página no encontrada - Error 404", 404


# ---------------------FUNCIONES--------------------------
def generate_non_recursive_rules(lista_reglas):
    resultado = []
    for i in range(0, len(lista_reglas) - 1):
        ruler = lista_reglas[i].replace(" ", "")  # Eliminar espacios en blanco
        simbolo_inicial = ruler[0]
        
        if len(lista_reglas[i]) < 4:
            error = ['La gramática está imcompleta']
            print(error)
            return render_template('app.html', resultado=error)

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
    print('resultado = ', resultado)

    return resultado