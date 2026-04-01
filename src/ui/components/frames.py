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
                     text_color="#080808").pack(pady=20)

        FrameCard(self, valor=len(pacientes),
                  descricao="Pacientes",
                  corner_radius=10
                  ).pack(pady=5)

        ctk.CTkLabel(self, text=f"Total de Atendimentos: {len(atendimentos)}",
                     text_color="#080808",
                     font=("Arial", 14)).pack(pady=5)

        ctk.CTkLabel(self, text=f"Atendimentos Hoje: {len(atend_hoje)}",
                     text_color="#080808",
                     font=("Arial", 14)).pack(pady=5)

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

