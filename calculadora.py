import tkinter as tk
from tkinter import messagebox

def calcular_cota_aprendiz(saldo_empregados: int, exclusoes: int) -> tuple:
    """
    Calcula a cota de aprendizes com base no saldo de empregados e exclusões.

    Args:
        saldo_empregados (int): Número total de empregados (incluindo exclusões).
        exclusoes (int): Número de empregados excluídos (por exemplo, cargos de direção).

    Returns:
        tuple: (cota_minima, cota_maxima)
    """
    # Saldo após exclusões
    saldo = saldo_empregados - exclusoes

    # Cálculo da cota mínima e máxima
    cota_minima = max(0.05 * saldo, 1)  # Pelo menos 1 aprendiz
    cota_maxima = 0.15 * saldo

    return cota_minima, cota_maxima

def calcular_cota_e_mostrar_resultado():
    try:
        # Obter os valores dos campos de entrada
        saldo_total_empregados = int(entrada_total_empregados.get())
        exclusoes_legais = int(entrada_exclusoes_legais.get())

        # Calcular a cota
        cota_min, cota_max = calcular_cota_aprendiz(saldo_total_empregados, exclusoes_legais)

        # Exibir os resultados em uma mensagem
        mensagem_resultado = f"Cota mínima de aprendizes: {cota_min:.2f}\nCota máxima de aprendizes: {cota_max:.2f}"
        messagebox.showinfo("Resultado", mensagem_resultado)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Calculadora de Cota de Aprendizes")

# Criar rótulos e campos de entrada
tk.Label(janela, text="Número total de funcionários:").pack()
entrada_total_empregados = tk.Entry(janela)
entrada_total_empregados.pack()

tk.Label(janela, text="Número de funcionários excluídos (exclusões legais):").pack()
entrada_exclusoes_legais = tk.Entry(janela)
entrada_exclusoes_legais.pack()

# Botão para calcular a cota
botao_calcular = tk.Button(janela, text="Calcular Cota", command=calcular_cota_e_mostrar_resultado)
botao_calcular.pack()

# Iniciar o loop principal da interface gráfica
janela.mainloop()
