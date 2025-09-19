import pandas as pd
import sqlite3

try:
    df_orders = pd.read_csv("northwind_orders.csv")
    df_order_details = pd.read_csv("northwind_order_details.csv")
    df_products = pd.read_csv("products.csv", encoding='latin1')
    df_customers = pd.read_csv("customers.csv", encoding='latin1')
    df_employees = pd.read_csv("employees.csv", encoding='latin1')
    print("-> Todos os arquivos principais foram carregados com sucesso!")
except FileNotFoundError as e:
    print(f"Erro! Arquivo não encontrado. Verifique se os CSVs estão na mesma pasta. Detalhe: {e}")
    exit()

#Order_date, shipped_date, required_date(object) e ship_region(NaN)
colunas_data_orders = ['order_date', 'required_date', 'shipped_date']
for coluna in colunas_data_orders:
    df_orders[coluna] = pd.to_datetime(df_orders[coluna])

df_orders['ship_region'] = df_orders['ship_region'].fillna('Desconhecido')

df_order_details['receita_linha'] = df_order_details['unit_price'] * df_order_details['quantity'] * (1 - df_order_details['discount'])
df_order_details['custo_linha'] = df_order_details['unit_price'] * df_order_details['quantity'] * 0.70
df_order_details['lucro_linha'] = df_order_details['receita_linha'] - df_order_details['custo_linha']

#SQL

nome_banco_dados = 'northwind.db'
conn = sqlite3.connect(nome_banco_dados)

dataframes_para_salvar = {
    'orders': df_orders,
    'order_details': df_order_details,
    'products': df_products,
    'customers': df_customers,
    'employees': df_employees
}

for nome_tabela, dataframe in dataframes_para_salvar.items():
    dataframe.to_sql(nome_tabela, conn, if_exists = 'replace', index = False)
    print(f"-> Tabela '{nome_tabela}' salva com sucesso!")

conn.close()
