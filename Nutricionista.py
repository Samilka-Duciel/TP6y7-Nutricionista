import sqlite3

# 2. Utilice clases que representen estos modelos (Paciente, Alimento, PlanComida).
class Paciente:
    def __init__(self, id, nombre, edad, peso_actual):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.peso_actual = peso_actual

class Alimento:
    def __init__(self, id, nombre, calorias):
        self.id = id
        self.nombre = nombre
        self.calorias = calorias

class PlanComidas:
    def __init__(self, id, paciente, alimento, fecha, cantidad):
        self.id = id
        self.paciente = paciente
        self.alimento = alimento
        self.fecha = fecha
        self.cantidad = cantidad

# 3. Emplee una clase repositorio (NutricionistaRepo) para manejar la persistencia de datos usando SQLite.
class NutricionistaRepo:
    def __init__(self, db_name='nutricionista.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    # 6. Use claves foráneas para asociar los planes con pacientes y alimentos.
    # -Inicialización de la base de datos: Crear la estructura de tablas al instanciar el repositorio.
    def create_table(self):
        with self.conn:
            self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS paciente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER CHECK (edad > 0),
                peso_actual REAL CHECK (peso_actual > 0)
            );
            CREATE TABLE IF NOT EXISTS alimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                calorias INTEGER CHECK (calorias > 0)
            ); 
            CREATE TABLE IF NOT EXISTS plan_comidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                alimento_id INTEGER,
                fecha TEXT NOT NULL,
                cantidad REAL CHECK (cantidad > 0),
                FOREIGN KEY (paciente_id) REFERENCES paciente (id),
                FOREIGN KEY (alimento_id) REFERENCES alimentos (id)
                UNIQUE (paciente_id, alimento_id, fecha, cantidad)
            );
        """)
    
    # 1. Permita registrar pacientes, alimentos y planes de comida.
    # 5. Permita hacer operaciones CRUD (crear, listar, actualizar, eliminar) sobre pacientes, alimentos y planes de comida.
    def agregar_paciente(self, nombre, edad, peso_actual):
        try:
            with self.conn:
                self.cursor.execute('INSERT INTO paciente (nombre, edad, peso_actual) VALUES (?, ?, ?)', 
                                    (nombre, edad, peso_actual))
        except sqlite3.Error as e:
            print(f"Error al agregar paciente: {e}")

    def agregar_alimento(self, nombre, calorias):
        try: 
            with self.conn:
                self.cursor.execute('INSERT INTO alimentos (nombre, calorias) VALUES (?, ?)', 
                                    (nombre, calorias))
        except sqlite3.Error as e:
            print(f"Error al agregar alimento: {e}")

    def agregar_plan_comidas(self, paciente_id, alimento_id, fecha, cantidad):
        try:
            with self.conn:
                existe = self.cursor.execute("""
                    SELECT COUNT(*) FROM plan_comidas
                    WHERE paciente_id = ? AND alimento_id = ? AND fecha = ? AND cantidad = ?
                    """, (paciente_id, alimento_id, fecha, cantidad)).fetchone()[0]
                if existe == 0:
                    self.cursor.execute('INSERT INTO plan_comidas (paciente_id, alimento_id, fecha, cantidad) VALUES (?, ?, ?, ?)', 
                                        (paciente_id, alimento_id, fecha, cantidad))
                else:
                    print("El plan de comidas ya existe.")
        except sqlite3.Error as e:
            print(f"Error al agregar plan de comidas: {e}")

    def listar_planes_comidas(self):
        with self.conn:
            planes = self.cursor.execute("""
                SELECT pc.id, p.id, p.nombre, p.edad, p.peso_actual, 
                       a.id, a.nombre, a.calorias, pc.fecha, pc.cantidad
                FROM plan_comidas pc
                JOIN paciente p ON pc.paciente_id = p.id
                JOIN alimentos a ON pc.alimento_id = a.id
            """).fetchall()
        
        return[
            PlanComidas(
                id=row[0],
                paciente=Paciente(id=row[1], nombre=row[2], edad=row[3], peso_actual=row[4]),
                alimento=Alimento(id=row[5], nombre=row[6], calorias=row[7]),
                fecha=row[8],
                cantidad=row[9]
            )
            for row in planes
        ]
    
    # -Actualizar el peso actual de un paciente (simulando un control de peso).
    def actualizar_peso_paciente(self, paciente_id, nuevo_peso):
        with self.conn:
            self.cursor.execute('UPDATE paciente SET peso_actual = ? WHERE id = ?', 
                                (nuevo_peso, paciente_id))
    
    # -Eliminar un plan de comida, luego eliminar el paciente.
    def eliminar_plan_comidas(self, plan_id):
        with self.conn:
            self.cursor.execute('DELETE FROM plan_comidas WHERE id = ?', (plan_id,))

    def eliminar_paciente(self, paciente_id):
        with self.conn:
            self.cursor.execute('DELETE FROM paciente WHERE id = ?', (paciente_id,))

    # 4. Implemente transacciones para asegurar la integridad en operaciones múltiples.
    # -Ejecutar una transacción donde se agregue un nuevo paciente, alimento y plan juntos. Si ocurre un error, nada debe persistirse.
    def ejecutar_transaccion(self, nombre_paciente, edad, peso, nombre_alimento, calorias, fecha, cantidad):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO paciente (nombre, edad, peso_actual) VALUES (?, ?, ?)', 
                               (nombre_paciente, edad, peso))
                paciente_id = cursor.lastrowid
                cursor.execute('INSERT INTO alimentos (nombre, calorias) VALUES (?, ?)', 
                               (nombre_alimento, calorias))
                alimento_id = cursor.lastrowid
                cursor.execute('INSERT INTO plan_comidas (paciente_id, alimento_id, fecha, cantidad) VALUES (?, ?, ?, ?)', 
                               (paciente_id, alimento_id, fecha, cantidad))
        except sqlite3.Error:
            self.conn.rollback()
            print("Error en la transacción, no se completó el cambio.")

    def verificar_duplicados(self):
        with self.conn:
            duplicados = self.cursor.execute("""
                SELECT paciente_id, alimento_id, fecha, cantidad, COUNT(*)
                FROM plan_comidas
                GROUP BY paciente_id, alimento_id, fecha, cantidad
                HAVING COUNT(*) > 1
            """).fetchall()
            
        if duplicados:
            print("Se encontraron duplicados en los planes de comida:")
            for registro in duplicados:
                print(f"Paciente ID: {registro[0]}, Alimento ID: {registro[1]}"), 
        else:
            print("No se encontraron duplicados en los planes de comida.")

    def eliminar_duplicados(self):
        with self.conn:
            self.cursor.execute("""
                DELETE FROM plan_comidas
                WHERE id NOT IN (
                    SELECT MIN(id) FROM plan_comidas
                    GROUP BY paciente_id, alimento_id, fecha, cantidad
                )
            """)
            print("Duplicados eliminados correctamente.")

 # -Agregar datos iniciales: Cargar algunos pacientes y alimentos con datos ficticios.
 # -Agregar un plan de comida: Registrar qué comió un paciente un día determinado, indicando la cantidad de alimento.

repo = NutricionistaRepo()
repo.agregar_paciente('Marcos', 30, 75.0)
repo.agregar_alimento('sandwich', 52)
repo.agregar_plan_comidas(1, 1, '2025-10-01', 2)
repo.verificar_duplicados()
repo.eliminar_duplicados()

#-Listar todos los planes de comida registrados, incluyendo:
#● Nombre del paciente
#● Nombre del alimento
#● Fecha
#● Cantidad
#● Calorías totales
planes = repo.listar_planes_comidas()
for plan in planes:
    calorias_totales = plan.cantidad * plan.alimento.calorias
    print(f"{plan.paciente.nombre} comió {plan.cantidad} de {plan.alimento.nombre} el {plan.fecha}.")

