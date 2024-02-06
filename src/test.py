import openpyxl

workbook_pokemons = openpyxl.load_workbook("src/assets/pokemons.xlsx")["Planilha1"]

print(workbook_pokemons[3][0].value)