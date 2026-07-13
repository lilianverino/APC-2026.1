import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
from utils.funcoes import gerar_conteudo_relatorio_geral, gerar_conteudo_relatorio
from utils.dicionario import DICIONARIO_RAS, FILE_PATH

total_registros = 0

class AppAnalise:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Explorador PDAD — Trabalho e Ocupação")
        self.janela.geometry("1000x850")
        
        self.df = None
        self.total_registros = 0
        self.lista_ras = []
        
        self.carregar_dados()
        self.criar_widgets()


    def carregar_dados(self):
        try:
            self.df = pd.read_csv(FILE_PATH, sep=";", low_memory=False)
            # numero de registros totais na planilha
            self.total_registros = len(self.df)

            # pegando os codigos das ras
            coluna_codigo_ra = "localidade" 

            if coluna_codigo_ra in self.df.columns:
                # Pega os códigos que existem com ctz estão na planilha (como texto e sem duplicados)
                codigos_reais = self.df[coluna_codigo_ra].dropna().unique().astype(str)
                lista_nomes = [nome for cod, nome in DICIONARIO_RAS.items() if cod in codigos_reais]
                self.lista_ras = sorted(lista_nomes)

            else:
                self.lista_ras = ["Coluna de códigos não encontrada!"]
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo:\n{e}")
            self.lista_ras = []

    def criar_widgets(self):
            #______________________________________________________-
            #cabeçalho do programa
            header_frame = tk.Frame(self.janela, bg="#2C3E50")
            header_frame.pack(fill="x", padx=0, pady=(0, 15))

            tk.Label(
                header_frame, 
                text="REGISTRO E — TRABALHO E OCUPAÇÃO", 
                font=("Arial", 16, "bold"), 
                bg="#2C3E50", 
                fg="#ECF0F1"
            ).pack(pady=(15, 5))

            tk.Label(
                header_frame, 
                text="Pergunta central: Como se distribui a população ocupada no DF? Quais setores de atividade predominam?", 
                font=("Arial", 10, "italic"), 
                bg="#2C3E50", 
                fg="#BDC3C7",
                wraplength=900
            ).pack(pady=(0, 15))
                
             #LEDENDAS
            legenda_frame = tk.LabelFrame(self.janela, text=" Informações do Projeto & Parâmetros ", font=("Arial", 10, "bold"), fg="#2C3E50")
            legenda_frame.pack(fill="x", padx=80, pady=10)

            # Adicionando as informações de autor, variáveis e escopo
            tk.Label(legenda_frame, text="Autor:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
            tk.Label(legenda_frame, text="Lilian Verino Lima", font=("Arial", 9)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            tk.Label(legenda_frame, text="Escopo:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
            tk.Label(legenda_frame, text="Análise de setores de atividade, cruzamento de ocupação por RA/Gênero e relação Escolaridade vs Renda.", font=("Arial", 9, "italic"), fg="#2980B9").grid(row=2, column=1, sticky="w", padx=5, pady=2)   
                
                
            #______________________________________________________-
            tk.Label(self.janela, text="Os dados abaixo levam em conta as primeiras 27 RAs do DF.", font=("Arial", 10)).pack(pady=10)
            tk.Label(self.janela, text="Selecione uma RA para filtrar:", font=("Arial", 10)).pack(pady=10)

            cor_contador = "#4ECE7A" if self.total_registros > 0 else "#D32F2F"
            tk.Label(self.janela, text=f"Registros carregados com sucesso: {self.total_registros}", font=("Arial", 10, "bold"), fg=cor_contador).pack(pady=5)

            self.combo_ras = ttk.Combobox(self.janela, values=self.lista_ras, state="readonly", width=30)
            self.combo_ras.pack(pady=5)
            if self.lista_ras:
                self.combo_ras.current(0)

            # Criamos uma variável booleana para rastrear se está marcado ou não
            self.salvar_arquivo_var = tk.BooleanVar(value=False) # Começa desmarcada
        
            self.chk_salvar = tk.Checkbutton(
                    self.janela, 
                    text="Baixar Relatório em .TXT automaticamente ao gerar", 
                    variable=self.salvar_arquivo_var,
                    font=("Arial", 10)
                )
            self.chk_salvar.pack(pady=5)

    
            # Criando um frame para os botões, para que fiquem lado a lado
            botoes_frame = tk.Frame(self.janela)
            botoes_frame.pack(fill="x", padx=80, pady=15)

            # Botão Geral (Coluna 0)
            tk.Button(
                botoes_frame, 
                text="Gerar Relatório Geral", 
                command=self.acao_botao_geral, 
                bg="#4CAF50", 
                fg="white", 
                font=("Arial", 10, "bold"),
                height=2
            ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

            # Botão Filtrado (Coluna 1)
            tk.Button(
                botoes_frame, 
                text="Gerar Relatório da RA Selecionada", 
                command=self.acao_botao_filtrar, 
                bg="#2196F3", 
                fg="white", 
                font=("Arial", 10, "bold"),
                height=2
            ).grid(row=0, column=1, sticky="ew", padx=(10, 0))

            # Configura as duas colunas do frame para expandirem igualmente
            botoes_frame.grid_columnconfigure(0, weight=1)
            botoes_frame.grid_columnconfigure(1, weight=1)
            self.lbl_relatorio = ScrolledText(self.janela, font=("Consolas", 11), wrap="word", bg="#F9F9F9", height=25)
            self.lbl_relatorio.pack(fill="both", expand=True, padx=80, pady=20)
            self.lbl_relatorio.configure(state='disabled')

# Funções dos Botões
    def acao_botao_filtrar( self):
        # Pega o nome selecionado na lista suspensa 
        nome_selecionado = self.combo_ras.get()
         #Busca reversa no dicionário para achar o código numérico 
        codigo_ra = next((cod for cod, nome in DICIONARIO_RAS.items() if nome == nome_selecionado), None)

        # Valida se encontrou o código
        if codigo_ra is None:
            self.atualizar_relatorio("Erro: Código da RA não encontrado.", "red")
            return

        # Chama a função passando o código encontrado e o seu DataFrame (df)
        relatorio_texto = gerar_conteudo_relatorio(codigo_ra, nome_selecionado, self.df) 
        # Mostra o resultado final direto na Label da janela
        if relatorio_texto:
            self.atualizar_relatorio(relatorio_texto, "black")
        else:
            self.atualizar_relatorio("Erro ao gerar o relatório.", "red")
            return
        
        #Verifica se a checkbox estiver marcada, exporta a RA específica
        if self.salvar_arquivo_var.get():
            # Deixa o nome do arquivo limpo (remove espaços e caracteres especiais do nome da RA)
            nome_arquivo_sugerido = f"Relatorio_{nome_selecionado.replace(' ', '_')}.txt"
            caminho_salvar = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")],
                initialfile=nome_arquivo_sugerido
            )
            if caminho_salvar:
                try:
                    with open(caminho_salvar, "w", encoding="utf-8") as arquivo:
                        arquivo.write(relatorio_texto)
                    messagebox.showinfo("Sucesso", f"Relatório de {nome_selecionado} exportado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")
        
    def acao_botao_geral(self):
        # adiciona o relatório na tela (Label)
        texto_final = gerar_conteudo_relatorio_geral(self.df)
        self.atualizar_relatorio(texto_final, "black")

        #Verifica se a checkbox de baixar está marcada (.get() retorna True ou False)
        if self.salvar_arquivo_var.get():
            caminho_salvar = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")],
                initialfile="Relatorio_Geral_Completo.txt"
            )
            if caminho_salvar:
                try:
                    with open(caminho_salvar, "w", encoding="utf-8") as arquivo:
                        arquivo.write(texto_final)
                    messagebox.showinfo("Sucesso", "Relatório Geral exportado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")

    def exportar_geral_para_txt(self):
            # Esta guarda em arquivo de texto externa
            texto_final = gerar_conteudo_relatorio_geral(self.df)
            caminho_salvar = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")],
                initialfile="Relatorio_Geral_Completo.txt"
            )
            if caminho_salvar:
                try:
                    with open(caminho_salvar, "w", encoding="utf-8") as arquivo:
                        arquivo.write(texto_final)
                    messagebox.showinfo("Sucesso", "Relatório Geral exportado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}") 

    def atualizar_relatorio(self, texto, cor):
        self.lbl_relatorio.configure(state='normal')
        self.lbl_relatorio.delete('1.0', tk.END)
        self.lbl_relatorio.insert(tk.END, texto)
        self.lbl_relatorio.configure(foreground=cor, state='disabled')

#Bloco q faz a janela abrir quando o script é executado diretamente
if __name__ == "__main__":
    root = tk.Tk()
    app = AppAnalise(root)
    root.mainloop() 
