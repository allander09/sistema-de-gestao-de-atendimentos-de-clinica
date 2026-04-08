import customtkinter as ctk
from .components.frames import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------------- CONFIGURAÇÃO PRINCIPAL ----------------
        self.title("Sistema de Gestão de Atendimentos e Clínica")
        self.geometry("1000x600")
        self.configure(bg_color="#ecf0f1")

        ctk.set_appearance_mode('dark')

        # ---------------- MENU LATERAL ----------------
        menu_frame = ctk.CTkFrame(self, bg_color="#2c3e50", width=00)
        menu_frame.pack(side="left", fill="y")

        # Título do sistema no menu
        logo = ctk.CTkLabel(
            menu_frame,
            text="Clínica\nGestão",
            text_color="#ecf0f1",
            font=("Arial", 24, "bold"),
            justify="center"
        )
        logo.pack(pady=20)


        # ---------------- BOTÕES DO MENU ----------------
        botoes = [
            "Dashboard",
            "Pacientes",
            "Atendimentos",
            "Novo Paciente",
            "Novo Atendimento"
        ]

        for nome in botoes:
            btn = ctk.CTkButton(
                menu_frame,
                text=nome,
                text_color="#080808",
                bg_color="#34495e",
                fg_color="white",
                font=("Arial", 14),
                hover_color="#1abc9c",
                height= 30,
                corner_radius=0,
                command=lambda n=nome: self.mostrar_tela(n)
            )
            btn.pack(fill="x", pady=5, padx=15)

        # Tela inicial
        #self.mostrar_tela("Dashboard")

        # ---------------- ÁREA DE CONTEÚDO ----------------
        self.content_frame = FrameDashboard(self, fg_color="#ecf0f1", corner_radius=0)
        self.content_frame.pack(side="right", expand=True, fill="both")
        
    


    # Função para trocar conteúdo
    def mostrar_tela(self, texto):
        self.content_frame.pack_forget()

        match texto:
            case "Dashboard":
                self.content_frame = FrameDashboard(self, fg_color="#ecf0f1", corner_radius=0)
                self.content_frame.pack(side="right", fill="x")
            case "Pacientes":
                self.content_frame = FrameListaPacientes(self, fg_color="#ecf0f1", corner_radius=2)
                self.content_frame.pack( expand=True, fill="both")
 
                
            case "Atendimentos":
                self.content_frame = FrameHistorico(self, fg_color="#ecf0f1", corner_radius=0)
                self.content_frame.pack(side="right", expand=True, fill="both")
                
                
            case "Novo Paciente":
                self.content_frame = FrameNovoPaciente(self, fg_color="#ecf0f1", corner_radius=0)
                self.content_frame.pack(side="right", expand=True, fill="both")

                
                ...
            case "Novo Atendimento":
                self.content_frame = FrameRegistroAtendimento(self, fg_color="#ecf0f1", corner_radius=0)
                self.content_frame.pack(side="right", expand=True, fill="both")

