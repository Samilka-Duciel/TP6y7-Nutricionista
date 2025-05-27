import tkinter as tk
from tkinter import ttk, messagebox
from Nutricionista import Paciente, Alimento, PlanComidas, NutricionistaRepo


class NutricionistaApp:
    def __init__(self, root, repo):
        self.repo = repo
        self.root = root
        self.root.title(" Gestión Nutricionista")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="aquamarine")
        style.map('TNotebook.Tab', background=[('selected', 'medium aquamarine')])
        style.configure("TButton", background="medium aquamarine")

        barra_superior = tk.Frame(root, bg="aquamarine")
        barra_superior.pack(fill="x")

        tk.Label(barra_superior, text="Gestión Nutricionista", font=("Arial", 18), bg="aquamarine", anchor="center").pack(fill="x", pady=10)
        frame_exterior = ttk.Frame(root)
        frame_exterior.pack(expand=1, fill="both")
        frame_espacio_izq = ttk.Frame(frame_exterior, width=200)
        frame_espacio_izq.pack(side="left", fill="y")
        
        frame_tabs = tk.Frame(frame_exterior, width=400, height=200, bg="white")
        frame_tabs.pack(side="left", expand=1, pady=(0, 100))
        frame_tabs.pack_propagate(False) 


        tab_control = ttk.Notebook(frame_tabs)
        self.tab_pacientes = ttk.Frame(tab_control)
        self.tab_alimentos = ttk.Frame(tab_control)
        self.tab_plan_comidas = ttk.Frame(tab_control)
        self.tab_listar = ttk.Frame(tab_control)
        tab_control.add(self.tab_pacientes, text="Pacientes")
        tab_control.add(self.tab_alimentos, text="Alimentos")
        tab_control.add(self.tab_plan_comidas, text="Plan de Comidas")
        tab_control.add(self.tab_listar, text="Listar Planes de Comidas")
        tab_control.pack(expand=1, fill="both")

        frame_espacio_der = ttk.Frame(frame_exterior, width=200)
        frame_espacio_der.pack(side="right", fill="y")

        # Pacientes
        ttk.Label(self.tab_pacientes, text="Nombre:").grid(row=0, column=0)
        self.nombre_entry = ttk.Entry(self.tab_pacientes)
        self.nombre_entry.grid(row=0, column=1)
        ttk.Label(self.tab_pacientes, text="Edad:").grid(row=1, column=0)
        self.edad_paciente = ttk.Entry(self.tab_pacientes)
        self.edad_paciente.grid(row=1, column=1)
        ttk.Label(self.tab_pacientes, text="Peso: ").grid(row=2, column=0)
        self.peso_paciente = ttk.Entry(self.tab_pacientes)
        self.peso_paciente.grid(row=2, column=1)
        ttk.Button(self.tab_pacientes, text="Agregar Paciente", command=self.agregar_paciente).grid(row=3, column=0, columnspan=2)

        # Alimentos
        ttk.Label(self.tab_alimentos, text="Nombre:").grid(row=0, column=0)
        self.nombre_alimento = ttk.Entry(self.tab_alimentos)
        self.nombre_alimento.grid(row=0, column=1)
        ttk.Label(self.tab_alimentos, text="Calorias:").grid(row=1, column=0)
        self.calorias_alimento = ttk.Entry(self.tab_alimentos)
        self.calorias_alimento.grid(row=1, column=1)
        ttk.Button(self.tab_alimentos, text="Agregar Alimento", command=self.agregar_alimento).grid(row=2, column=0, columnspan=2)

        #Plan de Comidas
        ttk.Label(self.tab_plan_comidas, text="Paciente ID:").grid(row=0, column=0)
        self.paciente_id = ttk.Entry(self.tab_plan_comidas)
        self.paciente_id.grid(row=0, column=1)
        ttk.Label(self.tab_plan_comidas, text="Alimento ID:").grid(row=1, column=0)
        self.alimento_id = ttk.Entry(self.tab_plan_comidas)
        self.alimento_id.grid(row=1, column=1)
        ttk.Label(self.tab_plan_comidas, text="Fecha:").grid(row=2, column=0)
        self.fecha = ttk.Entry(self.tab_plan_comidas)
        self.fecha.grid(row=2, column=1)
        ttk.Label(self.tab_plan_comidas, text="Cantidad:").grid(row=3, column=0)
        self.cantidad = ttk.Entry(self.tab_plan_comidas)
        self.cantidad.grid(row=3, column=1)
        ttk.Button(self.tab_plan_comidas, text="Agregar Plan de Comidas", command=self.agregar_plan_comidas).grid(row=4, column=0, columnspan=2)

        # Listar Planes de Comidas
        self.tree = ttk.Treeview(self.tab_listar, columns=("Paciente", "Alimento", "Fecha", "Cantidad", "Calorías Totales"), show="headings")
        for col in ("Paciente", "Alimento", "Fecha", "Cantidad", "Calorías Totales"):
            self.tree.heading(col, text=col)
        self.tree.pack(expand=1, fill="both")
        ttk.Button(self.tab_listar, text="Actualizar Lista", command=self.listar_planes).pack()
        self.listar_planes()

    def agregar_paciente(self):
        try:
            nombre = self.nombre_entry.get()
            edad = int(self.edad_paciente.get())
            peso = float(self.peso_paciente.get())
            self.repo.agregar_paciente(nombre, edad, peso)
            messagebox.showinfo("Éxito", "Paciente agregado exitosamente")
        except Exception:
            messagebox.showerror("Error", "Error al agregar paciente.")

    def agregar_alimento(self):
        try:
            nombre = self.nombre_alimento.get()
            calorias = int(self.calorias_alimento.get())
            self.repo.agregar_alimento(nombre, calorias)
            messagebox.showinfo("Éxito", "Alimento agregado exitosamente")
        except Exception:
            messagebox.showerror("Error", "Error al agregar alimento.")

    def agregar_plan_comidas(self):
        try:
            paciente_id = int(self.paciente_id.get())
            alimento_id = int(self.alimento_id.get())
            fecha = self.fecha.get()
            cantidad = float(self.cantidad.get())
            print(f"Intentando agregar plan: paciente_id={paciente_id}, alimento_id={alimento_id}, fecha={fecha}, cantidad={cantidad}")
            self.repo.agregar_plan_comidas(paciente_id, alimento_id, fecha, cantidad)
            messagebox.showinfo("Listo", "Plan de comidas agregado exitosamente")
        except Exception :
            messagebox.showerror("Verificar", "Error al agregar plan de comidas.")
    
    def listar_planes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        planes = self.repo.listar_planes_comidas()
        print("DEBUG planes:", planes)
        for plan in planes:
            calorias_totales = plan.cantidad * plan.alimento.calorias
            self.tree.insert("", "end", values=(
                plan.paciente.nombre, plan.alimento.nombre, plan.fecha, plan.cantidad, calorias_totales
            ))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    repo = NutricionistaRepo("nutricionista.db")
    app = NutricionistaApp(root, repo)
    root.mainloop()