import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")  # Sirve el formulario desde /templates

# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Obtener datos enviados desde el formulario
        data = request.json
        categoria = data.get("categoria")
        elemento = data.get("elemento")
        descripcion = data.get("descripcion")
        tipo = data.get("tipo")
        geometria = data.get("geometria")
        
        # Convertir `terreno` a cadena si es una lista
        terreno = data.get("terreno")
        if isinstance(terreno, list):
            terreno = ','.join(terreno)
        else:
            terreno = str(terreno) if terreno else None
        
        captacion = data.get("captacion")
        fotografias = data.get("fotografias")  # Esto será Base64
        observaciones = data.get("observaciones")

        # Conexión a la base de datos
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # Insertar datos en la tabla
        cur.execute("""
            INSERT INTO datos_btu_bim 
            (categoria, elemento_objeto, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (categoria, elemento, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Datos guardados con éxito"}), 200
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return jsonify({"error": f"Error al guardar los datos: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

