import customtkinter as ctk
from tkinter import ttk, messagebox



def tela_dashboard(self):
    for w in self.winfo_children():
        w.destroy()

    pacientes = carregar_dados(ARQ_PACIENTES)
    atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

    hoje = str(date.today())
    atend_hoje = [a for a in atendimentos if a["data"] == hoje]

    ctk.CTkLabel(self, text="Dashboard", font=("Arial", 22, "bold")).pack(pady=20)

    ctk.CTkLabel(self, text=f"Total de Pacientes: {len(pacientes)}",
                 font=("Arial", 14)).pack(pady=5)

    ctk.CTkLabel(self, text=f"Total de Atendimentos: {len(atendimentos)}",
                 font=("Arial", 14)).pack(pady=5)

    ctk.CTkLabel(self, text=f"Atendimentos Hoje: {len(atend_hoje)}",
                 font=("Arial", 14)).pack(pady=5)

''''
# ---------------- CADASTRO PACIENTE ----------------
def tela_novo_paciente(self):
    for w in self.winfo_children():
        w.destroy()

    campos = {}

    def salvar():
        dados = carregar_dados(ARQ_PACIENTES)

        paciente = {
            "nome": campos["Nome"].get(),
            "data_nascimento": campos["Nascimento"].get(),
            "telefone": campos["Telefone"].get(),
            "email": campos["Email"].get(),
            "documento": campos["Documento"].get()
        }

        dados.append(paciente)
        salvar_dados(ARQ_PACIENTES, dados)

        messagebox.showinfo("Sucesso", "Paciente cadastrado!")
        tela_pacientes(self)

    labels = ["Nome", "Nascimento", "Telefone", "Email", "Documento"]

    for i, l in enumerate(labels):
        ctk.CTkLabel(self, text=l).grid(row=i, column=0, pady=5, padx=10)
        e = tk.Entry(self, width=30)
        e.grid(row=i, column=1)
        campos[l] = e

    tk.Button(self, text="Salvar", bg="#1abc9c",
              command=salvar).grid(row=6, columnspan=2, pady=20)


# ---------------- LISTA + BUSCA ----------------
def tela_pacientes(self):
    for w in self.winfo_children():
        w.destroy()

    dados = carregar_dados(ARQ_PACIENTES)

    ctk.CTkLabel(self, text="Pacientes", font=("Arial", 20, "bold")).pack(pady=10)

    busca = tk.Entry(self)
    busca.pack()

    tree = ttk.Treeview(self, columns=("Nome", "Telefone"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Telefone", text="Telefone")
    tree.pack(fill="both", expand=True)

    def carregar(lista):
        tree.delete(*tree.get_children())
        for p in lista:
            tree.insert("", "end", values=(p["nome"], p["telefone"]))

    def filtrar(event):
        texto = busca.get().lower()
        filtrados = [
            p for p in dados
            if texto in p["nome"].lower() or texto in p["telefone"]
        ]
        carregar(filtrados)

    busca.bind("<KeyRelease>", filtrar)
    carregar(dados)

    def selecionar():
        item = tree.selection()
        if not item:
            return
        nome = tree.item(item)["values"][0]
        tela_atendimento(self, nome)

    tk.Button(self, text="Registrar Atendimento",
              command=selecionar).pack(pady=10)


# ---------------- ATENDIMENTO ----------------
def tela_atendimento(self, nome_paciente):
    for w in self.winfo_children():
        w.destroy()

    campos = {}

    ctk.CTkLabel(self, text=f"Atendimento - {nome_paciente}",
                 font=("Arial", 18)).pack(pady=10)

    labels = ["Data", "Tipo", "Observações", "Status"]

    for l in labels:
        ctk.CTkLabel(self, text=l).pack()
        e = tk.Entry(self, width=40)
        e.pack()
        campos[l] = e

    campos["Data"].insert(0, str(date.today()))

    def salvar():
        dados = carregar_dados(ARQ_ATENDIMENTOS)

        atendimento = {
            "paciente": nome_paciente,
            "data": campos["Data"].get(),
            "tipo": campos["Tipo"].get(),
            "observacoes": campos["Observações"].get(),
            "status": campos["Status"].get()
        }

        dados.append(atendimento)
        salvar_dados(ARQ_ATENDIMENTOS, dados)

        messagebox.showinfo("Sucesso", "Atendimento registrado!")
        tela_pacientes(self)

    tk.Button(self, text="Salvar", bg="#1abc9c",
              command=salvar).pack(pady=10)

    tk.Button(self, text="Ver Histórico",
              command=lambda: tela_historico(self, nome_paciente)).pack()


# ---------------- HISTÓRICO ----------------
def tela_historico(self, nome):
    for w in self.winfo_children():
        w.destroy()

    dados = carregar_dados(ARQ_ATENDIMENTOS)
    filtrados = [a for a in dados if a["paciente"] == nome]

    ctk.CTkLabel(self, text=f"Histórico - {nome}",
                 font=("Arial", 18)).pack(pady=10)

    tree = ttk.Treeview(self,
                        columns=("Data", "Tipo", "Status"),
                        show="headings")

    for c in ("Data", "Tipo", "Status"):
        tree.heading(c, text=c)

    tree.pack(fill="both", expand=True)

    for a in filtrados:
        tree.insert("", "end",
                    values=(a["data"], a["tipo"], a["status"]))


# ---------------- MENU ----------------
botoes = [
    ("Dashboard", tela_dashboard),
    ("Pacientes", tela_pacientes),
    ("Novo Paciente", tela_novo_paciente)
]

for nome, func in botoes:
    tk.Button(menu_frame, text=nome, bg="#34495e", fg="white",
              relief="flat", command=lambda f=func: f(root)).pack(fill="x", pady=5, padx=10)

# Inicial
tela_dashboard()

root.mainloop()
'''