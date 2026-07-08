import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd

# 1. Carregar os dados
file_path = r"c:\Users\User\Desktop\APC-2026.1\Semana15\moradores.csv"

# === DICIONÁRIO DE MAPEAMENTO ===
# Substitua os números abaixo pelos códigos reais da sua planilha
# e coloque o nome correto de cada Região Administrativa.
DICIONARIO_RAS = {
    "5301": "Plano Piloto",
    "5302": "Gama",
    "5303": "Taguatinga",
    "5304": "Brazlândia",
    "5305": "Sobradinho",
    "5306": "Planaltina",
    "5307": "Paranoá",
    "5308": "Núcleo Bandeirante",
    "5309": "Ceilândia",
    "5310": "Guará",
    "5311": "Cruzeiro",
    "5312": "Samambaia",    
    "5313": "Santa Maria",
    "5314": "São Sebastião",    
    "5315": "Recanto das Emas",
    "5316": "Lago Sul",
    "5317": "Riacho Fundo",
    "5318": "Lago Norte",
    "5319": "Candangolândia",
    "5320": "Águas Claras",
    "5321": "Riacho Fundo II",
    "5322": "Sudoeste/Octogonal",
    "5323": "Varjão",
    "5324": "Park Way",
    "5325": "SCIA (Setor Complementar de Indústria e Abastecimento)",
    "5326": "Sobradinho II",
    "5327": "Jardim Botânico",
}

ESCOLARIDADE = {
    1:"Sem instrução", 2:"Fund. incompleto", 3:"Fund. completo",
    4:"Médio incompleto", 5:"Médio completo", 6:"Superior incompleto",
    7:"Superior completo", 8:"Pós-graduação"
}
total_registros = 0
try:
    df = pd.read_csv(file_path, sep=";", low_memory=False)
    # numero de registros totais na planilha
    total_registros = len(df)

    # pegando os codigos das ras
    coluna_codigo_ra = "localidade" 

    if coluna_codigo_ra in df.columns:
        # Pega os códigos que existem com ctz estão na planilha (como texto e sem duplicados)
        codigos_reais_planilha = (
            df[coluna_codigo_ra].dropna().unique().astype(str)
        )

        # Cria a lista filtrada: SÓ adiciona o nome se o código estiver no dicionário
        # E se ele realmente existir dentro da planilha
        lista_nomes_janela = []
        for codigo, nome in DICIONARIO_RAS.items():
            if codigo in codigos_reais_planilha:
                lista_nomes_janela.append(nome)

        # Ordena em ordem alfabética
        lista_ras = sorted(lista_nomes_janela)
    else:
        lista_ras = ["Coluna de códigos não encontrada!"]
        print("Colunas encontradas:", df.columns.tolist())

except Exception as e:
    messagebox.showerror("Erro", f"Erro ao carregar o arquivo:\n{e}")
    lista_ras = []

def insertion_sort_escolaridade(lista):
    # Ordena pela chave (1 a 8)
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j]['nivel_num'] > chave['nivel_num']:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


def gerar_conteudo_relatorio(ra_codigo, ra_nome, moradores_df):
    # Filtra os dados com base no código da RA
    # (Note que forcei o tipo para string para evitar erros caso o CSV leia como texto)
    filtro = moradores_df[moradores_df["localidade"].astype(str) == str(ra_codigo)]

    if filtro.empty:
        return f"Nenhum dado encontrado para a RA: {ra_nome} (Código: {ra_codigo})"

    # Processa Escolaridade
    contagem = {}
    for n in filtro["escolaridade"]:
        if n in ESCOLARIDADE:
            contagem[n] = contagem.get(n, 0) + 1

    lista_esc = [
        {"nivel": ESCOLARIDADE[k], "nivel_num": k, "total": v}
        for k, v in contagem.items()
    ]

    # Ordena usando a sua função de ordenação
    lista_esc = insertion_sort_escolaridade(lista_esc)

    #separando por genero, retirando os desconhecidos ou não declarados
    codigos_para_excluir = [99999, 88888, 77777]

    # filtrando generos
    homem = filtro[(filtro["E03_1"] == 1) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    mulher = filtro[(filtro["E03_1"] == 2) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    homemtrans = filtro[(filtro["E03_1"] == 3) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    mulhertrans = filtro[(filtro["E03_1"] == 4) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    agenero = filtro[(filtro["E03_1"] == 5) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    generoqueer = filtro[(filtro["E03_1"] == 6) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    generofluido = filtro[(filtro["E03_1"] == 7) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    nbinario = filtro[(filtro["E03_1"] == 8) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    travesti = filtro[(filtro["E03_1"] == 9) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    transmasc = filtro[(filtro["E03_1"] == 10) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    transfem = filtro[(filtro["E03_1"] == 11) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    outro = filtro[(filtro["E03_1"] == 12) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()

    # variavel de genero por RA
    linhas_moradores_por_ra = ["--- Distribuição de Moradores por RA ---"]
    total_geral_validos = 0

    for codigo_ra, nome_ra in DICIONARIO_RAS.items():
        moradores_da_ra = filtro[filtro["localidade"].astype(str) == str(codigo_ra)]
        total_ra = len(moradores_da_ra)
        total_geral_validos += total_ra
        
        # loop for para listar todas
        if total_ra > 0:
            linhas_moradores_por_ra.append(f" * {nome_ra:<22}: {total_ra} moradores")
   
   # Filtro para calcular a idade (revolvendo quem tem código desconhecido)
    filtro_idade = filtro[filtro["idade_calculada"] != 99999]
    
    # Se a lista não estiver vazia, calcula a média, senão deixa 0
    media_idade = filtro_idade["idade_calculada"].mean() if not filtro_idade.empty else 0
    
    # Porcentagem de Mulheres Cis em relação ao total de moradores da RA
    total_moradores = len(filtro)
    porcentagem_mulheres = (len(mulher) / total_moradores * 100) if total_moradores > 0 else 0

    linhas_moradores_por_ra.append(f" Total Geral Válido     : {total_geral_validos}")
    linhas_moradores_por_ra.append("----------------------------------------")
    
    # Junta as RAs 
    texto_ras = "\n".join(linhas_moradores_por_ra)

    # Monta o relatório em formato de texto
    linhas = [f"Relatório da RA: {ra_nome}", "=" * 40]
    linhas.append(f"Total moradores: {len(filtro)}")
    linhas.append(f"Total moradores: {len(filtro)}")
    linhas.append(f"Média de Idade: {media_idade:.1f} anos")
    linhas.append(f"Representação Feminina (cis): {porcentagem_mulheres:.1f}% do total")
    linhas.append(f"Homens cis: {len(homem)}")
    linhas.append(f"Mulheres cis: {len(mulher)}")
    linhas.append(f"Homens trans: {len(homemtrans)}")
    linhas.append(f"Mulheres trans: {len(mulhertrans)}")
    linhas.append(f"Agênero: {len(agenero)}")
    linhas.append(f"Gênero Queer: {len(generoqueer)}")
    linhas.append(f"Gênero Fluido: {len(generofluido)}")
    linhas.append(f"Não-Binário: {len(nbinario)}")
    linhas.append(f"Travesti: {len(travesti)}")
    linhas.append(f"Trans Masculino: {len(transmasc)}")
    linhas.append(f"Trans Feminino: {len(transfem)}")
    linhas.append(f"Outro: {len(outro)}")

    linhas.append("\nEscolaridade (Ordenada por nível):")
    for item in lista_esc:
        linhas.append(f" - {item['nivel']}: {item['total']}")

    return "\n".join(linhas)


# função relatório geral 

def gerar_conteudo_relatorio_geral(moradores_df):
    filtro = moradores_df[moradores_df["idade_calculada"] != 99999].copy()
    
    if filtro.empty:
        return "Nenhum dado válido encontrado na planilha para o relatório geral."

    total_geral_validos = len(filtro)

    # Calcula a média da coluna idade_calculada
    media_idade_geral = filtro["idade_calculada"].mean()

    # Processa Escolaridade
    contagem = {}
    for n in filtro["escolaridade"]:
        if n in ESCOLARIDADE:
            contagem[n] = contagem.get(n, 0) + 1

    lista_esc = [
        {"nivel": ESCOLARIDADE[k], "nivel_num": k, "total": v}
        for k, v in contagem.items()
    ]
    lista_esc = insertion_sort_escolaridade(lista_esc)

    # Filtrando gêneros globalmente
    codigos_para_excluir = [99999, 88888, 77777]
    homem = filtro[(filtro["E03_1"] == 1) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    mulher = filtro[(filtro["E03_1"] == 2) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    homemtrans = filtro[(filtro["E03_1"] == 3) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    mulhertrans = filtro[(filtro["E03_1"] == 4) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    agenero = filtro[(filtro["E03_1"] == 5) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    generoqueer = filtro[(filtro["E03_1"] == 6) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    generofluido = filtro[(filtro["E03_1"] == 7) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    nbinario = filtro[(filtro["E03_1"] == 8) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    travesti = filtro[(filtro["E03_1"] == 9) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    transmasc = filtro[(filtro["E03_1"] == 10) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    transfem = filtro[(filtro["E03_1"] == 11) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()
    outro = filtro[(filtro["E03_1"] == 12) & (~filtro["E03_1"].isin(codigos_para_excluir))].copy()

   # porcentagem de mulheres cis baseada no total de dados conhecidos 
    porcentagem_mulheres_geral = (len(mulher) / total_geral_validos * 100) if total_geral_validos > 0 else 0

    #  Distribuição por RA
    linhas_moradores_por_ra = ["--- Distribuição de Moradores por RA ---"]
    total_calculado_ras = 0

    for codigo_ra, nome_ra in DICIONARIO_RAS.items():
        moradores_da_ra = filtro[filtro["localidade"].astype(str) == str(codigo_ra)]
        total_ra = len(moradores_da_ra)
        total_calculado_ras += total_ra
        
        if total_ra > 0:
            linhas_moradores_por_ra.append(f" * {nome_ra:<22}: {total_ra} moradores")
   
    linhas_moradores_por_ra.append(f" Total Mapeado por RAs  : {total_calculado_ras}")
    linhas_moradores_por_ra.append("----------------------------------------")
    
    texto_ras = "\n".join(linhas_moradores_por_ra)

    # Monta o relatório em formato de texto integrando as médias e porcentagens
    relatorio_completo = ["Relatório Geral:", "=" * 40]            
    relatorio_completo.append(texto_ras) 
    
    # Adicionando os novos dados estatísticos no topo do bloco de dados demográficos
    relatorio_completo.append(f"Total de registros válidos : {total_geral_validos}")
    relatorio_completo.append(f"Média de Idade Geral       : {media_idade_geral:.1f} anos")
    relatorio_completo.append(f"Proporção de Mulheres Cis  : {porcentagem_mulheres_geral:.1f}%")
    relatorio_completo.append("-" * 40)
    relatorio_completo.append(f"Homens cis: {len(homem)}")
    relatorio_completo.append(f"Mulheres cis: {len(mulher)}")
    relatorio_completo.append(f"Homens trans: {len(homemtrans)}")
    relatorio_completo.append(f"Mulheres trans: {len(mulhertrans)}")
    relatorio_completo.append(f"Agênero: {len(agenero)}")
    relatorio_completo.append(f"Gênero Queer: {len(generoqueer)}")
    relatorio_completo.append(f"Gênero Fluido: {len(generofluido)}")
    relatorio_completo.append(f"Não-Binário: {len(nbinario)}")
    relatorio_completo.append(f"Travesti: {len(travesti)}")
    relatorio_completo.append(f"Trans Masculino: {len(transmasc)}")
    relatorio_completo.append(f"Trans Feminino: {len(transfem)}")
    relatorio_completo.append(f"Outro: {len(outro)}")

    relatorio_completo.append("\nEscolaridade (Ordenada por nível):")
    for item in lista_esc:
        relatorio_completo.append(f" - {item['nivel']}: {item['total']}")

    return "\n".join(relatorio_completo)



# Funções dos Botões
def acao_botao_filtrar():
    # Pega o nome selecionado na lista suspensa 
    nome_selecionado = combo_ras.get()

    #Busca reversa no dicionário para achar o código numérico 
    codigo_ra = None
    for cod, nome in DICIONARIO_RAS.items():
        if nome == nome_selecionado:
            codigo_ra = cod
            break

    # Valida se encontrou o código
    if codigo_ra is None:
        lbl_relatorio.config(text="Erro: Código da RA não encontrado.")
        return

    # Chama a função passando o código encontrado e o seu DataFrame (df)
    relatorio_texto = gerar_conteudo_relatorio(codigo_ra, nome_selecionado, df)

    # Mostra o resultado final direto na Label da janela
    if relatorio_texto:
        lbl_relatorio.config(text=relatorio_texto, fg="black")
    else:
        lbl_relatorio.config(text="Erro ao gerar o relatório.", fg="red")

def acao_botao_geral():
    # aciona o relatório na tela (Label)
    texto_final = gerar_conteudo_relatorio_geral(df)
    lbl_relatorio.config(text=texto_final, fg="black")


def exportar_geral_para_txt():
    # Esta guarda em arquivo de texto externa
    texto_final = gerar_conteudo_relatorio_geral(df)
    
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


# Interface Gráfica
janela = tk.Tk()
janela.title("Sistema de Análise de RA: Trabalho e Ocupação")
janela.state('zoomed')

lbl_recorte = tk.Label(
    janela, text="Os dados abaixo levam em conta as primeiras 27 RAs do DF.", font=("Arial", 10)
)
lbl_recorte.pack(pady=10)

lbl_instrucao = tk.Label(
    janela, text="Selecione uma RA para filtrar:", font=("Arial", 10)
)
lbl_instrucao.pack(pady=10)



#total de registros
lbl_contador = tk.Label(
    janela, 
    text=f"Registros carregados com sucesso: {total_registros}", 
    font=("Arial", 10, "bold"),
    fg="#4ECE7A" if total_registros > 0 else "#D32F2F" # Fica verde se carregou ou vermelho se deu erro
)
lbl_contador.pack(pady=5)

# Lista Suspensa agora exibe os nomes em ordem alfabética
combo_ras = ttk.Combobox(janela, values=lista_ras, state="readonly", width=30)
combo_ras.pack(pady=5)
if lista_ras:
    combo_ras.current(0)

tk.Label(janela, text="").pack(pady=5)


# botão q dá os resultados por ra
btn_filtrar = tk.Button(
    janela,
    text="Gerar Relatório da RA Selecionada abaixo",
    command=acao_botao_filtrar,  
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_filtrar.pack(fill="x", padx=80, pady=40)

# botão q dá os relatorio completo por txt
btn_geral = tk.Button(
    janela,
    text="Gerar Relatório Geral",
    command=acao_botao_geral,  #  ação que joga na Label
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_geral.pack(fill="x", padx=80, pady=10)

# botão q exporta o relatorio completo por txt
btn_baixar_txt = tk.Button(
    janela,
    text="Baixar Relatório Geral em .TXT",
    command=exportar_geral_para_txt,  # Chama a função de salvar arquivo
    bg="#FF9800",                     
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_baixar_txt.pack(fill="x", padx=80, pady=5)


#  ScrolledText pq ficou mt grande para uma Label só, e assim o usuário pode rolar a tela
lbl_relatorio = ScrolledText(
    janela, 
    font=("Consolas", 11), 
    wrap="word",     # Faz o texto quebrar a linha por palavra se for muito largo
    bg="#F9F9F9",    # Cor de fundo levemente cinza 
    height=25        # Altura inicial em número de linhas
)
lbl_relatorio.pack(fill="both", expand=True, padx=80, pady=20)

janela.mainloop()