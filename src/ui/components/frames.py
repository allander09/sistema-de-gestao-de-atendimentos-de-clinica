import customtkinter as ctk
from ...utils.utils import *
from datetime import date

# ---------------- DASHBOARD ----------------
class FrameDashboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        hoje = str(date.today())
        atend_hoje = [a for a in atendimentos if a["data"] == hoje]

        ctk.CTkLabel(self, text="Dashboard", font=("Arial", 22, "bold"),
                     text_color="#080808").grid(row=0, column=0, columnspan=2)
        
        #frame_cards = ctk.CTkFrame(self).pack(padx=10, pady=10)

        FrameCard(self, valor=len(pacientes),
                  descricao="Pacientes",
                  corner_radius=10
                  ).grid(row=1, column=0)
        
        FrameCard(self, valor=35, descricao='Atendimentos', corner_radius=10
                  ).grid(row=1, column=1)
        
        FrameCard(self, valor=15, descricao='Atendimentos do Dia', corner_radius=10
                  ).grid(row=1, column=2)


#------------------- pacientes----------------------
class FrameListaPacientes(ctk.CTkFrame):
    def __init__(self, master, selecionar_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.selecionar_callback = selecionar_callback

        ctk.CTkLabel(self, text="Pacientes",
                     font=("Arial", 20, "bold")).pack(pady=10)

        self.busca = ctk.CTkEntry(self, placeholder_text="Buscar por nome ou telefone")
        self.busca.pack(pady=5)

        ctk.CTkButton(self, text="Buscar", command=self.listar).pack(pady=5)

        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(fill="both", expand=True, pady=10)

        self.listar()

    def listar(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        pacientes = carregar_dados(ARQ_PACIENTES)
        termo = self.busca.get().lower()

        for p in pacientes:
            if termo in p["nome"].lower() or termo in p["telefone"]:
                btn = ctk.CTkButton(
                    self.frame_lista,
                    text=f"{p['nome']} - {p['telefone']}",
                    command=lambda paciente=p: self.selecionar(paciente)
                )
                btn.pack(pady=2, fill="x")

    def selecionar(self, paciente):
        if self.selecionar_callback:
            self.selecionar_callback(paciente) 

#----------------atendimento---------------- 

class FrameHistorico(ctk.CTkFrame):
    def __init__(self, master,paciente=None, **kwargs):
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self,
                     text=f"Histórico - {paciente['id_nome']}",
                     font=("Arial", 18, "bold")).pack(pady=10)

        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        lista = [a for a in atendimentos if a["paciente_id"] == paciente["id"]]

        for a in lista:
            texto = f"{a['data']} - {a['tipo']} ({a['status']})"
            ctk.CTkLabel(self, text=texto).pack(pady=2)

#--------------novo paciente--------------
class FrameNovoPaciente(ctk.CTkFrame):
    def __init__(self, master, atualizar_lista_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.atualizar_lista_callback = atualizar_lista_callback

        ctk.CTkLabel(self,
                     text="Novo Paciente",
                     font=("Arial", 20, "bold"),
                     text_color="#080808").pack(pady=15)

        self.nome = ctk.CTkEntry(self, placeholder_text="Nome completo")
        self.nome.pack(pady=5, fill="x", padx=20)

        self.nascimento = ctk.CTkEntry(self, placeholder_text="Data de nascimento")
        self.nascimento.pack(pady=5, fill="x", padx=20)

        self.telefone = ctk.CTkEntry(self, placeholder_text="Telefone")
        self.telefone.pack(pady=5, fill="x", padx=20)

        self.email = ctk.CTkEntry(self, placeholder_text="E-mail")
        self.email.pack(pady=5, fill="x", padx=20)

        self.documento = ctk.CTkEntry(self, placeholder_text="CPF ou RG")
        self.documento.pack(pady=5, fill="x", padx=20)

        ctk.CTkButton(self,
                      text="Salvar Paciente",
                      command=self.salvar).pack(pady=15)

    def salvar(self):
        pacientes = carregar_dados(ARQ_PACIENTES)

        novo_paciente = {
            "nome": self.nome.get(),
            "nascimento": self.nascimento.get(),
            "telefone": self.telefone.get(),
            "email": self.email.get(),
            "documento": self.documento.get()
        }

        pacientes.append(novo_paciente)
        salvar_dados(ARQ_PACIENTES, pacientes)

        # Limpar campos
        self.nome.delete(0, "end")
        self.nascimento.delete(0, "end")
        self.telefone.delete(0, "end")
        self.email.delete(0, "end")
        self.documento.delete(0, "end")

        # Atualizar lista (se existir)
        if self.atualizar_lista_callback:
            self.atualizar_lista_callback()

#--------- novo atendimento------------

class FrameRegistroAtendimento(ctk.CTkFrame):
    def __init__(self, master, paciente=None, **kwargs):
        super().__init__(master, **kwargs)

        self.paciente = paciente

        ctk.CTkLabel(self, text="Registrar Atendimento",
                     font=("Arial", 20, "bold")).pack(pady=10)

        self.tipo = ctk.CTkEntry(self, placeholder_text="Tipo de atendimento")
        self.tipo.pack(pady=5)

        self.obs = ctk.CTkEntry(self, placeholder_text="Observações")
        self.obs.pack(pady=5)

        self.status = ctk.CTkOptionMenu(self,
                                       values=["realizado", "em acompanhamento"])
        self.status.pack(pady=5)

        ctk.CTkButton(self, text="Salvar", command=self.salvar).pack(pady=10)

    def salvar(self):
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        novo = {
            "paciente": self.paciente["nome"],
            "data": str(date.today()),
            "tipo": self.tipo.get(),
            "observacoes": self.obs.get(),
            "status": self.status.get()
        }

        atendimentos.append(novo)
        salvar_dados(ARQ_ATENDIMENTOS, atendimentos)




# ---------------- CARDS ----------------
class FrameCard(ctk.CTkFrame):
    def __init__(self, master, valor, descricao, **kwargs):
        super().__init__(master, **kwargs)

        self.valor = ctk.CTkLabel(self, text=valor, font=("D-DIN-Bold", 30, "bold"),
                     text_color="white")
        self.descricao = ctk.CTkLabel(self, text=descricao, font=("D-DIN-Bold", 18, "bold"),
                     text_color="white")
        
        self.valor.pack(padx=10, pady=(10, 0), anchor='w')
        self.descricao.pack(padx=10, pady=(0, 10), anchor='w')

  