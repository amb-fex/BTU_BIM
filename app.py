import psycopg2
from flask import Flask, request, jsonify, render_template
import base64

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Conexión a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")

# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Obtener datos enviados desde el formulario
        data = request.get_json()  # Asegura que los datos se reciban como JSON
        if not data:
            return jsonify({"error": "No se recibió un JSON válido"}), 400

        # Validar campos obligatorios
        required_fields = ["categoria", "elemento", "tipo", "geometria", "terreno", "fotografias"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo obligatorio: {field}"}), 400

        # Extraer y procesar datos
        categoria = data["categoria"]
        elemento = data["elemento"]
        descripcion = data.get("descripcion", "")
        tipo = data["tipo"]
        geometria = data["geometria"]
        terreno = ",".join(data["terreno"])  # Convierte la lista en una cadena separada por comas
        captacion = data.get("captacion", "")
        observaciones = data.get("observaciones", "")

        # Convertir fotografias de Base64 a bytes
        try:
            fotografias = base64.b64decode(data["fotografias"])
        except Exception as e:
            return jsonify({"error": f"Error al procesar el campo 'fotografias': {e}"}), 400

        # Insertar datos en la base de datos
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO datos_btu_bim 
            (categoria, elemento_objeto, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (categoria, elemento, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones),
        )
        conn.commit()
        cur.close()

        return jsonify({"message": "Datos guardados con éxito"}), 200

    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)