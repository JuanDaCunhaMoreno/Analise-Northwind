import pandas as pd
import sqlite3

conn = sqlite3.connect('northwind.db')

print("--- Ranking de Funcionários por Receita Gerada ---")

consulta_funcionarios = """
SELECT
    e.employeeName AS Funcionario, 
    SUM(od.receita_linha) AS Receita_Total
FROM
    employees AS e
INNER JOIN orders AS o ON e.employeeID = o.employee_id -- Ajustamos o nome da coluna de ID aqui também
INNER JOIN order_details AS od ON o.order_id = od.order_id
GROUP BY
    Funcionario
ORDER BY
    Receita_Total DESC;
"""

df_funcionarios = pd.read_sql_query(consulta_funcionarios, conn)
print(df_funcionarios)
df_funcionarios.to_csv('ranking_funcionarios.csv', index = False)

print("\n--- Ranking de Clientes por Lucro Gerado ---")

consulta_clientes = """
SELECT
    c.companyName AS Cliente,
    SUM(od.lucro_linha) AS Lucro_Total
FROM
    customers AS c
INNER JOIN orders AS o ON c.customerID = o.customer_id
INNER JOIN order_details AS od ON o.order_id = od.order_id
GROUP BY
    Cliente
ORDER BY
    Lucro_Total DESC
LIMIT 15;
"""

df_clientes = pd.read_sql_query(consulta_clientes, conn)

df_clientes.to_csv('ranking_clientes_lucro.csv', index=False)
print(df_clientes)

print("\n--- Análise de Produtos Críticos (Baixo Estoque vs. Alta Demanda) ---")

consulta_inventario = """
-- CTE para calcular a demanda (número de pedidos por produto)
WITH DemandaProdutos AS (
    SELECT
        product_id,
        COUNT(order_id) AS numero_de_pedidos
    FROM
        order_details
    GROUP BY
        product_id
)
-- Consulta principal para ranquear os produtos mais pedidos
SELECT
    p.productName AS Produto, 
    dp.numero_de_pedidos AS Total_de_Pedidos
FROM
    products AS p
INNER JOIN DemandaProdutos AS dp ON p.productID = dp.product_id 
ORDER BY
    Total_de_Pedidos DESC;
"""

df_inventario = pd.read_sql_query(consulta_inventario, conn)

df_inventario.to_csv('analise_inventario.csv', index=False)
print(df_inventario)

print("\n--- Calculando KPIs Financeiros Globais (Receita, Custo, Lucro) ---")

consulta_kpis = """
SELECT
    SUM(receita_linha) AS Receita_Total,
    SUM(custo_linha) AS Custo_Total,
    SUM(lucro_linha) AS Lucro_Total
FROM
    order_details;
"""

df_kpis = pd.read_sql_query(consulta_kpis, conn)

# Salvar o resultado para o Power BI
df_kpis.to_csv('kpis_financeiros.csv', index=False)
print(df_kpis)

conn.close()
