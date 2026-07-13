import pandas as pd
from utils.dicionario import DICIONARIO_I13, DICIONARIO_RAS, ESCOLARIDADE, CODIGOS_PARA_EXCLUIR

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

#relatorio por RA
def gerar_conteudo_relatorio(ra_codigo, ra_nome, moradores_df, setor_filtro=None):
    # Forçando o tipo para string para evitar erros caso o CSV leia como texto
    filtro = moradores_df[moradores_df["localidade"].astype(str) == str(ra_codigo)]

    # Filtragem por setor (se o usuário escolher um)
    if setor_filtro and setor_filtro != "Todos" and col_posicao in filtro.columns:
        filtro = filtro[filtro[col_posicao].astype(str) == str(setor_filtro)]

    if filtro.empty:
        return f"Nenhum dado encontrado para a RA: {ra_nome} (Código: {ra_codigo})"
    
    #Identificação automática das suas colunas reais
    col_renda = "renda_ind_r" if "renda_ind_r" in moradores_df.columns else ("renda_ind" if "renda_ind" in moradores_df.columns else None)
    col_posicao = "I13" if "I13" in moradores_df.columns else None

    # Processa Escolaridade e Renda Combinadas
    contagem = {}
    rendas_por_nivel = {}
    
    for _, row in filtro.iterrows():
        n_raw = row["escolaridade"]
       #Identifica a escolaridade mesmo se for int, float ou string
        n = None

        if n_raw in ESCOLARIDADE:
            n = n_raw
        else:
            try:
                n_int = int(float(n_raw))
                if n_int in ESCOLARIDADE:
                    n = n_int
                elif str(n_int) in ESCOLARIDADE:
                    n = str(n_int)
            except (ValueError, TypeError):
                n_str = str(n_raw).strip()
                if n_str in ESCOLARIDADE:
                    n = n_str

        if n in ESCOLARIDADE:
            contagem[n] = contagem.get(n, 0) + 1
            
        # Captura a renda real corrigida se ela existir e for válida
            if col_renda:
                val_renda = row[col_renda]
                try:
                    val_num = float(val_renda)
                    # Comparações seguras usando números puros

                    if isinstance(val_renda, str):
                        val_renda = val_renda.replace(',', '.').strip()
                    
                    val_num = float(val_renda)

                    # Mude de >= 0 para > 0
                    if pd.notna(val_num) and int(val_num) not in CODIGOS_PARA_EXCLUIR and val_num > 0:  
                        if n not in rendas_por_nivel:
                            rendas_por_nivel[n] = []
                        rendas_por_nivel[n].append(val_num)
                except (ValueError, TypeError):
                    # Ignora linhas com textos inválidos na renda
                    pass     

     # Monta a lista calculando a média salarial
    lista_esc = []
    for k, v in contagem.items():
        rendas = rendas_por_nivel.get(k, [])
        renda_media = sum(rendas) / len(rendas) if rendas else 0.0
        lista_esc.append({
            "nivel": ESCOLARIDADE[k], 
            "nivel_num": k, 
            "total": v,
            "renda_media": renda_media,
            "tem_renda": len(rendas) > 0,
            "qtd_respostas_renda": len(rendas)
        })
    # Cria a lista de dicionários para ordenação
    # Ordena usando a sua função de ordenação
    lista_esc = insertion_sort_escolaridade(lista_esc)

    #separando por genero, retirando os desconhecidos ou não declarados
    #codigos_para_excluir = [99999, 88888, 77777]

    # filtrando generos
    homem = filtro[(filtro["E03_1"] == 1) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    mulher = filtro[(filtro["E03_1"] == 2) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    homemtrans = filtro[(filtro["E03_1"] == 3) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    mulhertrans = filtro[(filtro["E03_1"] == 4) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    agenero = filtro[(filtro["E03_1"] == 5) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    generoqueer = filtro[(filtro["E03_1"] == 6) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    generofluido = filtro[(filtro["E03_1"] == 7) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    nbinario = filtro[(filtro["E03_1"] == 8) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    travesti = filtro[(filtro["E03_1"] == 9) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    transmasc = filtro[(filtro["E03_1"] == 10) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    transfem = filtro[(filtro["E03_1"] == 11) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    outro = filtro[(filtro["E03_1"] == 12) & (~filtro["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()

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

    linhas_moradores_por_ra.append(f" Total Geral Conhecidos     : {total_geral_validos}")
    linhas_moradores_por_ra.append("----------------------------------------")
    
    # ... (Seu código original de cálculo de idade e porcentagem)
    media_idade = filtro_idade["idade_calculada"].mean() if not filtro_idade.empty else 0
    porcentagem_mulheres = (len(mulher) / total_moradores * 100) if total_moradores > 0 else 0
    # Junta as RAs 
    texto_ras = "\n".join(linhas_moradores_por_ra)

    # ==========================================
    # Tradução e contagem da Posição na Ocupação (I13)
    linhas_posicao = ["\nPosição na Ocupação Predominante (I13):"]
    if col_posicao and col_posicao in filtro.columns:
        top_posicoes = filtro[col_posicao].value_counts().head(5)
        for codigo, qtd in top_posicoes.items():
            try:
                cod_int = int(codigo)
            except ValueError:
                cod_int = codigo
            if cod_int in [88888, 99999]: # Pula respostas inválidas
                continue
            nome_posicao = DICIONARIO_I13.get(cod_int, f"Código {codigo}")
            pct_pos = (qtd / total_moradores) * 100
            linhas_posicao.append(f" - {nome_posicao}: {qtd} pessoas ({pct_pos:.1f}%)")
    else:
        linhas_posicao.append(" - Informação de posição na ocupação não disponível.")

    # ==========================================
    # Monta o relatório em formato de texto 
    linhas = [f"Relatório da RA: {ra_nome}", "=" * 40]
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

   # Injeta o bloco de ocupação traduzido aqui
    linhas.extend(linhas_posicao)

    # Exibição da Escolaridade combinada com a Renda Média Real
    linhas.append("\nEscolaridade (Ordenada por nível):")
    for item in lista_esc:
        if item['tem_renda']:
            # Exibe a média e avisa sobre quantas pessoas geraram aquele valor
            renda_formatada = f"Renda média de R$ {item['renda_media']:.2f} (com base em {item['qtd_respostas_renda']} pessoa(s))"
        else:
            renda_formatada = f"Não Declarada (0 de {item['total']} pessoas responderam)"
            
        linhas.append(f" - {item['nivel']}: {item['total']} moradores no total | {renda_formatada}")
    return "\n".join(linhas)


# função relatório geral 
def gerar_conteudo_relatorio_geral(moradores_df):
    
    if moradores_df.empty:
        return "Nenhum dado encontrado no arquivo para gerar o relatório geral."

# Identificação automática das suas colunas reais
    col_renda = "renda_ind_r" if "renda_ind_r" in moradores_df.columns else ("renda_ind" if "renda_ind" in moradores_df.columns else None)
    col_posicao = "I13" if "I13" in moradores_df.columns else None
    # Processa Escolaridade e Renda Real Combinadas (Para o DF inteiro)
    contagem = {}
    rendas_por_nivel = {}
    
    for _, row in moradores_df.iterrows():
        n_raw = row["escolaridade"]  
        # Identifica a escolaridade mesmo se for int, float ou string
        n = None

        if n_raw in ESCOLARIDADE:
            n = n_raw
        else:
            try:
                n_int = int(float(n_raw))
                if n_int in ESCOLARIDADE:
                    n = n_int
                elif str(n_int) in ESCOLARIDADE:
                    n = str(n_int)
            except (ValueError, TypeError):
                n_str = str(n_raw).strip()
                if n_str in ESCOLARIDADE:
                    n = n_str

        if n in ESCOLARIDADE:
            contagem[n] = contagem.get(n, 0) + 1
            
            # Captura a renda real corrigida se ela existir e for válida
            if col_renda:
                val_renda = row[col_renda]
                try:
                    val_num = float(val_renda)
                    # Comparações seguras usando números puros

                    if isinstance(val_renda, str):
                        val_renda = val_renda.replace(',', '.').strip()
                    
                    val_num = float(val_renda)

                    # Mude de >= 0 para > 0
                    if pd.notna(val_num) and int(val_num) not in CODIGOS_PARA_EXCLUIR and val_num > 0:  
                        if n not in rendas_por_nivel:
                            rendas_por_nivel[n] = []
                        rendas_por_nivel[n].append(val_num)
                except (ValueError, TypeError):
                    # Ignora linhas com textos inválidos na renda
                    pass

    lista_esc = []
    for k, v in contagem.items():
        rendas = rendas_por_nivel.get(k, [])
        renda_media = sum(rendas) / len(rendas) if rendas else 0.0
        lista_esc.append({
            "nivel": ESCOLARIDADE[k], 
            "nivel_num": k, 
            "total": v, 
            "renda_media": renda_media,
            "tem_renda": len(rendas) > 0,
            "qtd_respostas_renda": len(rendas)
        })

    # Ordena usando a sua função de ordenação
    lista_esc = insertion_sort_escolaridade(lista_esc)

    # Filtrando gêneros globalmente
    homem = moradores_df[(moradores_df["E03_1"] == 1) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    mulher = moradores_df[(moradores_df["E03_1"] == 2) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    homemtrans = moradores_df[(moradores_df["E03_1"] == 3) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    mulhertrans = moradores_df[(moradores_df["E03_1"] == 4) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    agenero = moradores_df[(moradores_df["E03_1"] == 5) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    generoqueer = moradores_df[(moradores_df["E03_1"] == 6) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    generofluido = moradores_df[(moradores_df["E03_1"] == 7) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    nbinario = moradores_df[(moradores_df["E03_1"] == 8) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    travesti = moradores_df[(moradores_df["E03_1"] == 9) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    transmasc = moradores_df[(moradores_df["E03_1"] == 10) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    transfem = moradores_df[(moradores_df["E03_1"] == 11) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()
    outro = moradores_df[(moradores_df["E03_1"] == 12) & (~moradores_df["E03_1"].isin(CODIGOS_PARA_EXCLUIR))].copy()



    # Tabela resumo de moradores por RA
    linhas_moradores_por_ra = ["--- Distribuição de Moradores por RA ---"]
    total_geral_validos = 0

    for codigo_ra, nome_ra in DICIONARIO_RAS.items():
        moradores_da_ra = moradores_df[moradores_df["localidade"].astype(str) == str(codigo_ra)]
        total_ra = len(moradores_da_ra)
        total_geral_validos += total_ra
        
        if total_ra > 0:
            linhas_moradores_por_ra.append(f" * {nome_ra:<22}: {total_ra} moradores")
   
    # Filtro para calcular a idade no DF inteiro
    filtro_idade = moradores_df[moradores_df["idade_calculada"] != 99999]
    media_idade_geral = filtro_idade["idade_calculada"].mean() if not filtro_idade.empty else 0
   
   # porcentagem de mulheres cis baseada no total de dados conhecidos 
    porcentagem_mulheres_geral = (len(mulher) / total_geral_validos * 100) if total_geral_validos > 0 else 0
    total_moradores = len(moradores_df)
    porcentagem_mulheres = (len(mulher) / total_moradores * 100) if total_moradores > 0 else 0

    linhas_moradores_por_ra.append(f" Total Mapeado por RAs  : {total_geral_validos}")
    linhas_moradores_por_ra.append("----------------------------------------")
    
    texto_ras = "\n".join(linhas_moradores_por_ra)

     # ==========================================
    # Tradução e contagem da Posição na Ocupação (I13)
    linhas_posicao_geral = ["\nPosição na Ocupação Predominante:"]
    if col_posicao and col_posicao in moradores_df.columns:
        top_posicoes = moradores_df[col_posicao].value_counts().head(5)
        for codigo, qtd in top_posicoes.items():
            try:
                cod_int = int(codigo)
            except ValueError:
                cod_int = codigo
            if cod_int in [88888, 99999]:
                continue
            nome_posicao = DICIONARIO_I13.get(cod_int, f"Código {codigo}")
            pct_pos = (qtd / total_moradores) * 100
            linhas_posicao_geral.append(f" - {nome_posicao}: {qtd} pessoas ({pct_pos:.1f}%)")
    else:
        linhas_posicao_geral.append(" - Informação de posição na ocupação (I13) não disponível.")

 # ==========================================
    # Monta o relatório em formato de texto integrando as médias e porcentagens
    relatorio_completo = ["Relatório Geral:", "=" * 40]            
    relatorio_completo.append(texto_ras) 
    
    # Adicionando os novos dados estatísticos no topo do bloco de dados demográficos
    relatorio_completo.append(f"Total de registros conhecidos : {total_geral_validos}")
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
   # Injeta a listagem de ocupações do DF
    relatorio_completo.extend(linhas_posicao_geral)

    # Exibição da Escolaridade combinada com a Renda Média Real do DF
    relatorio_completo.append("\nEscolaridade Geral vs Renda Média Real:")
    for item in lista_esc:
        if item['tem_renda']:
            # Exibe a média e avisa sobre quantas pessoas geraram aquele valor
            renda_formatada = f"Renda média de R$ {item['renda_media']:.2f} (com base em {item['qtd_respostas_renda']} pessoa(s))"
        else:
            renda_formatada = f"Não Declarada (0 de {item['total']} pessoas responderam)"
            
        relatorio_completo.append(f" - {item['nivel']}: {item['total']} moradores no total | {renda_formatada}")
    return "\n".join(relatorio_completo)
