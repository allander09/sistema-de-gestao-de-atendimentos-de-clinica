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
                     text_color="#080808").pack(pady=10)
        
        frame_cards = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)

        FrameCard(frame_cards, valor=len(pacientes),
                  descricao="Pacientes",
                  corner_radius=10
                  ).pack(pady=10, padx=10, fill="both", expand=True, side='left')
        
        FrameCard(frame_cards, valor=len(atendimentos), descricao='Atendimentos', corner_radius=10
                  ).pack(pady=10, padx=10, fill="both", expand=True, side='left')
        
        
        FrameCard(frame_cards, valor=len(atend_hoje), descricao='Atendimentos do Dia', corner_radius=10
                  ).pack(pady=10, padx=10, fill="both", expand=True, side='left')
        
        frame_cards.pack(padx=20, fill="x")
        


#------------------- pacientes----------------------
class FrameListaPacientes(ctk.CTkFrame):
    def __init__(self, master, selecionar_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.selecionar_callback = selecionar_callback
        
        frame_input = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)

        ctk.CTkLabel(self, text="Pacientes", font=("Arial", 22, "bold"),
                     text_color="#080808").pack(pady=10)

        self.busca = ctk.CTkEntry(frame_input, placeholder_text="Buscar por nome ou telefone")
        self.busca.pack(pady=10, padx=10, fill="both", expand=True, side='left')

        ctk.CTkButton(frame_input, text="Buscar", height=40,command=self.listar).pack(pady=10, padx=10, side='left')

        self.frame_lista = ctk.CTkScrollableFrame(self, fg_color="#f0f0f0", corner_radius=10)
        
        self.listar()

        frame_input.pack(padx=20, fill="x")
        self.frame_lista.pack(fill="both", expand=True, pady=10)

        

    def listar(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        pacientes = carregar_dados(ARQ_PACIENTES)
        termo = self.busca.get().lower()

        for p in pacientes:
            if termo in p["nome"].lower() or termo in p["telefone"]:
                card = FrameCardPacientes(self.frame_lista, nome=p["nome"], data_nascimento=p["data_nascimento"],
                                            telefone=p["telefone"], email=p["email"], corner_radius=10)
                card.pack(pady=5, padx=20, fill="x")
            

    def selecionar(self, paciente):
        if self.selecionar_callback:
            self.selecionar_callback(paciente) 

#----------------atendimento---------------- 

class FrameHistorico(ctk.CTkFrame):
    def __init__(self, master, paciente=None, **kwargs):
        super().__init__(master, **kwargs)

        if not paciente:
            ctk.CTkLabel(
                self,
                text="Nenhum paciente selecionado",
                font=("Arial", 18, "bold"),
                text_color="black"
            ).pack(pady=20)
            return

        nome = paciente.get("id_nome", "Paciente")

        ctk.CTkLabel(
            self,
            text=f"Histórico - {nome}",
            font=("Arial", 18, "bold"),
            text_color="black"
        ).pack(pady=10)
        
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        lista = [
            a for a in atendimentos
            if a.get("paciente_id") == paciente.get("id")
        ]

        if not lista:
            ctk.CTkLabel(
                self,
                text="Nenhum atendimento encontrado",
                text_color="black"
            ).pack(pady=10)
            return

        for a in lista:
            texto = f"{a.get('data', '---')} - {a.get('tipo', '---')} ({a.get('status', '---')})"
            ctk.CTkLabel(self, text=texto, text_color="black").pack(pady=2)
#--------------novo paciente--------------
class FrameNovoPaciente(ctk.CTkFrame):
    def __init__(self, master, atualizar_lista_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.atualizar_lista_callback = atualizar_lista_callback

        ctk.CTkLabel(self,
                     text="Novo Paciente",
                     font=("Arial", 20, "bold"),
                     text_color="#080808").pack(pady=15)

        self.nome = ctk.CTkEntry(self, placeholder_text="Nome completo", height=40, font=("Arial", 14))
        self.nome.pack(pady=10, fill="x", padx=100)

        self.frame_tel_data = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        self.nascimento = ctk.CTkEntry(self.frame_tel_data, placeholder_text="Data de nascimento", height=40, font=("Arial", 14))
        self.telefone = ctk.CTkEntry(self.frame_tel_data, placeholder_text="Telefone", height=40, font=("Arial", 14))

        self.frame_tel_data.pack(pady=10, fill="x", padx=100)
        self.telefone.pack(pady=10, padx=(0, 5), fill="both", side='left', expand=True)
        self.nascimento.pack(pady=10, padx=(0, 5), fill="both", side='left', expand=True)


        self.email = ctk.CTkEntry(self, placeholder_text="E-mail", height=40, font=("Arial", 14))
        self.email.pack(pady=10, fill="x", padx=100)

        self.frame_doc = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        self.tipo_documento = ctk.CTkOptionMenu(self.frame_doc, values=["CPF", "RG"], height=40, font=("Arial", 14))
        self.documento = ctk.CTkEntry(self.frame_doc, placeholder_text="Preencha o campo", height=40, font=("Arial", 14))
        
        self.tipo_documento.pack(pady=10, padx=(0, 5), fill="x", side='left')
        self.documento.pack(pady=10, padx=(0, 5), fill="both", side='left', expand=True)
        self.frame_doc.pack(pady=10, fill="x", padx=100)


        ctk.CTkButton(self,
                      text="Cadastrar",
                      command=self.salvar, height=40).pack(pady=15)
        
    def salvar(self):
        pacientes = carregar_dados(ARQ_PACIENTES)

        novo_paciente = {
            "id": len(pacientes) + 1,
            "nome": self.nome.get(),
            "data_nascimento": self.nascimento.get(),
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
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.frame_atendimento = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)

        ctk.CTkLabel(self.frame_atendimento, text="Registrar Atendimento",
                     text_color="#080808",font=("Arial", 20, "bold")).pack(pady=10)
        
        self.paciente_id = ctk.CTkEntry(self.frame_atendimento, placeholder_text="ID do paciente", height=40, font=("Arial", 14))
        self.paciente_id.pack(pady=10, fill="x", padx=100)

        self.tipo = ctk.CTkOptionMenu(self.frame_atendimento, values=["Consulta", "Exame", "Tratamento"], height=40, font=("Arial", 14))
        self.tipo.pack(pady=10, fill="x", padx=100)

        ctk.CTkLabel(self.frame_atendimento, text="Observações", font=("Arial", 14), text_color="#272525").pack(padx=100, anchor='w')
        self.obs = ctk.CTkTextbox(self.frame_atendimento, fg_color="black", height=100)
        self.obs.pack(pady=10, fill="x", padx=100)

        self.status = ctk.CTkOptionMenu(self.frame_atendimento,
                                       values=["Realizado", "Em Acompanhamento", "agendado"], height=40, font=("Arial", 14))
        self.status.pack(pady=(10, 0), fill="x", padx=100)

        ctk.CTkButton(self.frame_atendimento, text="Salvar", command=self.salvar, height=40, font=("Arial", 14)).pack(pady=10)

        self.frame_atendimento.pack(padx=20, pady=20, fill="x")

    def salvar(self):
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        paciente_id = self.paciente_id.get()

        novo = {
            "paciente_id": paciente_id,
            "data": str(date.today()),
            "tipo": self.tipo.get(),
            "observacoes": self.obs.get("1.0", "end").strip(),
            "status": self.status.get()
        }

        atendimentos.append(novo)
        salvar_dados(ARQ_ATENDIMENTOS, atendimentos)



    def ir_para_historico(self, paciente_id):
        pacientes = carregar_dados(ARQ_PACIENTES)

        paciente = next(
            (p for p in pacientes if str(p.get("id")) == str(paciente_id)),
            None
        )

        # limpar tela atual
        for widget in self.master.winfo_children():
            widget.destroy()

        # abrir histórico
        FrameHistorico(self.master, paciente=paciente).pack(fill="both", expand=True)

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

class FrameCardPacientes(ctk.CTkFrame):
    def __init__(self, master, nome, data_nascimento, telefone, email, **kwargs):
        super().__init__(master, **kwargs)

        data = data_nascimento.split("-")
        data_nascimento = f"{data[2]}/{data[1]}/{data[0]}"

        self.nome = ctk.CTkLabel(self, text=nome, font=("D-DIN-Bold", 18, "bold"),
                     text_color="#f0f0f0")
        self.data_nascimento = ctk.CTkLabel(self, text=f"Nascimento: {data_nascimento}", font=("D-DIN-Bold", 14),
                     text_color="#f0f0f0")
        self.telefone = ctk.CTkLabel(self, text=f"Telefone: {telefone}", font=("D-DIN-Bold", 14),
                     text_color="#f0f0f0")
        self.email = ctk.CTkLabel(self, text=f"E-mail: {email}", font=("D-DIN-Bold", 14),
                     text_color="#f0f0f0")
        
        self.nome.pack(padx=10, pady=(10, 0), anchor='w')
        self.data_nascimento.pack(padx=10, pady=(0, 0), anchor='w')
        self.telefone.pack(padx=10, pady=(0, 0), anchor='w')
        self.email.pack(padx=10, pady=(0, 10), anchor='w')