# Carregando os dados
FILE_PATH = r"c:\Users\User\Desktop\APC-2026.1\Semana15\pdad-explorer-lilian\dados\moradores.csv"

# dicionario com os nomes das ras
DICIONARIO_RAS = {
    "5301": "Plano Piloto", "5302": "Gama", "5303": "Taguatinga", "5304": "Brazlândia", "5305": "Sobradinho", 
    "5306": "Planaltina", "5307": "Paranoá", "5308": "Núcleo Bandeirante", "5309": "Ceilândia", "5310": "Guará",
    "5311": "Cruzeiro", "5312": "Samambaia", "5313": "Santa Maria", "5314": "São Sebastião", "5315": "Recanto das Emas",
    "5316": "Lago Sul", "5317": "Riacho Fundo", "5318": "Lago Norte", "5319": "Candangolândia", "5320": "Águas Claras",
    "5321": "Riacho Fundo II", "5322": "Sudoeste/Octogonal", "5323": "Varjão","5324": "Park Way",
    "5325": "SCIA (Setor Complementar de Indústria e Abastecimento)", "5326": "Sobradinho II", "5327": "Jardim Botânico",
}

DICIONARIO_I13 = {
    1: "Empregado no setor público",
    2: "Militar do exército/marinha/aeronáutica",
    3: "Empregado no setor privado",
    4: "Empregado Doméstico",
    5: "Estágio Remunerado",
    6: "Aprendiz",
    7: "Conta Própria ou Autônomo",
    8: "Empregador",
    9: "Presta Serviço Militar Obrigatório",
    10: "Trabalhador não remunerado"
}

ESCOLARIDADE = {
    1:"Sem instrução", 2:"Fund. incompleto", 3:"Fund. completo",
    4:"Médio incompleto", 5:"Médio completo", 6:"Superior incompleto",
    7:"Superior completo", 8:"Pós-graduação"
}

#separando por genero, retirando os desconhecidos ou não declarados
CODIGOS_PARA_EXCLUIR = [99999, 88888, 77777]