import tkinter as tk
from PIL import Image, ImageTk
from monster import createMonster


class MonsterCreatorApp:
    def __init__(self, root):
        self.root = root
        self.configurar_janela()
        self.campos_visiveis = False
        self.carregar_widgets()

    def configurar_janela(self):
        self.root.title("Criador de Monstros RPG")
        largura_janela = 1024
        altura_janela = 800
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x_central = int((largura_tela - largura_janela) / 2)
        y_central = int((altura_janela - largura_janela) / 2)
        self.root.geometry(f"{largura_janela}x{altura_janela}+{x_central}+{y_central}")
        self.root.resizable(False, False)

        self.background_image = ImageTk.PhotoImage(Image.open("assets/background.png"))
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

    def carregar_widgets(self):
        self.carregar_botoes()
        self.validation_message = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12, "italic"),
            bg="#2b2b2b",
            fg="#FFFFFF",
        )
        self.validation_message.place(relx=0.5, rely=0.9, anchor="center")
        self.validation_message.place_forget()

    def criar_entradas(self):
        self.frame_entradas = tk.Frame(self.root, bg="#2b2b2b")
        self.frame_entradas.place(relx=0.5, rely=0.4, anchor="center")

        self.nome_label, self.nome_entry = self.criar_campo("Nome do Monstro", 0)
        self.elemento_label, self.elemento_entry = self.criar_campo("Tipo de Elemento (fogo, água, terra, ar)", 1)
        self.vida_label, self.vida_entry = self.criar_campo("Pontos de Vida (50-200)", 2)
        self.habilidades_label, self.habilidades_entry = self.criar_campo("Habilidades (separadas por vírgulas)", 3)

        self.botao_criar = tk.Button(
            self.root,
            text="Criar Monstro",
            font=("Helvetica", 16, "bold"),
            bg="#555555",
            fg="#AAAAAA",
            state="disabled",
            command=self.criar_monstro,
        )
        self.botao_criar.place(relx=0.5, rely=0.7, anchor="center")

    def criar_campo(self, texto, row):
        label = tk.Label(
            self.frame_entradas,
            text=texto,
            font=("Helvetica", 14),
            bg="#2b2b2b",
            fg="#FFD700",
        )
        label.grid(row=row, column=0, padx=10, pady=10, sticky="w")

        entry = tk.Entry(
            self.frame_entradas,
            font=("Helvetica", 14),
            width=40,
            bg="#1E1E1E",
            fg="#FFD700",
            insertbackground="#FFD700",
            highlightthickness=2,
            highlightbackground="#388E3C",
            highlightcolor="#66BB6A",
        )
        entry.grid(row=row, column=1, padx=10, pady=10)
        entry.bind("<KeyRelease>", self.verificar_inputs)
        return label, entry

    def verificar_inputs(self, event=None):
        nome = self.nome_entry.get().strip()
        elemento = self.elemento_entry.get().strip().lower()
        vida = self.vida_entry.get().strip()
        habilidades = self.habilidades_entry.get().strip()

        if not nome:
            self.mostrar_validacao("O nome do monstro não pode estar vazio.")
        elif elemento not in {"fogo", "água", "terra", "ar"}:
            self.mostrar_validacao("Tipo de elemento inválido. Use fogo, água, terra ou ar.")
        elif not vida.isdigit() or not (50 <= int(vida) <= 200):
            self.mostrar_validacao("Os pontos de vida devem estar entre 50 e 200.")
        elif not habilidades:
            self.mostrar_validacao("Adicione pelo menos uma habilidade.")
        else:
            self.ocultar_validacao()
            self.botao_criar.config(bg="#1B5E20", fg="#FFD700", state="normal")
            return

        self.botao_criar.config(bg="#555555", fg="#AAAAAA", state="disabled")

    def mostrar_validacao(self, mensagem):
        self.validation_message.config(text=mensagem)
        self.validation_message.place(relx=0.5, rely=0.9, anchor="center")

    def ocultar_validacao(self):
        self.validation_message.place_forget()

    def carregar_botoes(self):
        self.icon_add = ImageTk.PhotoImage(Image.open("assets/add.png").resize((50, 50)))
        self.icon_exit = ImageTk.PhotoImage(Image.open("assets/exit.png").resize((50, 50)))

        self.create_hover_button(self.root, self.icon_add, "Adicionar Monstro", self.mostrar_entradas, 0.35)
        self.create_hover_button(self.root, self.icon_exit, "Sair", self.sair, 0.65)

    def create_hover_button(self, root, icon, tooltip_text, command, relx_position):
        button = tk.Button(
            root,
            image=icon,
            command=command,
            bg="#0D3A16",
            activebackground="#1B5E20",
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        button.place(relx=relx_position, rely=0.9, anchor="center")

        tooltip = tk.Label(
            root,
            text=tooltip_text,
            font=("Helvetica", 10, "italic"),
            bg="#2b2b2b",
            fg="#FFD700",
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=2,
        )
        tooltip.place_forget()

        def on_enter(e):
            button.config(bg="#1B5E20", relief="raised")
            tooltip.place(relx=relx_position, rely=0.85, anchor="center")

        def on_leave(e):
            button.config(bg="#0D3A16", relief="flat")
            tooltip.place_forget()

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def criar_monstro(self):
        nome = self.nome_entry.get().strip()
        elemento = self.elemento_entry.get().strip()
        vida = int(self.vida_entry.get().strip())
        habilidades = [h.strip() for h in self.habilidades_entry.get().strip().split(",")]

        try:
            monstro = createMonster(nome, elemento, vida, habilidades)
            descricao = f"🌟 Monstro Criado com Sucesso! 🌟\n\nNome: {monstro['name']}\nElemento: {monstro['element']}\nVida: {monstro['health']}\nHabilidades: {', '.join(monstro['skills'])}\n"
            self.exibir_saida(descricao)
        except ValueError as e:
            self.exibir_saida(f"Erro: {e}")

    def exibir_saida(self, texto):
        self.output_frame = tk.Frame(self.root, bg="#2b2b2b", highlightthickness=2, highlightbackground="#388E3C")
        self.output_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.text_output = tk.Text(
            self.output_frame,
            font=("Courier", 14),
            width=80,
            height=10,
            state="normal",
            bg="#2b2b2b",
            fg="#FFD700",
            highlightthickness=0,
        )
        self.text_output.pack(side="left", fill="both", expand=True)
        self.text_output.insert(tk.END, texto)
        self.text_output.configure(state="disabled")

        self.close_output_button = tk.Button(
            self.output_frame,
            text="✖",
            font=("Helvetica", 12, "bold"),
            bg="#2b2b2b",
            fg="#FFD700",
            bd=0,
            command=self.fechar_saida,
        )
        self.close_output_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

    def fechar_saida(self):
        self.output_frame.place_forget()
        self.ocultar_campos()
        self.mostrar_inicio()

    def ocultar_campos(self):
        if hasattr(self, "frame_entradas"):
            self.frame_entradas.place_forget()
        if hasattr(self, "botao_criar"):
            self.botao_criar.place_forget()
        self.campos_visiveis = False

    def mostrar_inicio(self):
        self.carregar_botoes()

    def mostrar_entradas(self):
        if not self.campos_visiveis:
            self.criar_entradas()
            self.campos_visiveis = True
        self.frame_entradas.place(relx=0.5, rely=0.4, anchor="center")

    def sair(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MonsterCreatorApp(root)
    root.mainloop()
