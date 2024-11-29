import customtkinter as ctk
from tkinter import filedialog, messagebox


# Função para processar os dados com precisão de 6 dígitos e remover duplicatas de tempo
def process_data(data):
    processed_data = []
    seen_times = set()

    for line in data.splitlines():
        columns = line.strip().split(',')
        if len(columns) >= 6:
            time = float(columns[0])
            thrust = float(columns[5])

            if time in seen_times:
                processed_data = [entry for entry in processed_data if not entry.startswith(f"{time:.6f}")]
            
            seen_times.add(time)
            processed_data.append(f"{time:.6f} {thrust:.6f}")

    return processed_data

# Função para salvar os dados processados
def salvar_arquivo():
    dados = caixa_texto.get("1.0", "end").strip()
    if not dados:
        messagebox.showerror("Erro", "A caixa de texto está vazia! Insira os dados.")
        return

    caminho_saida = filedialog.asksaveasfilename(
        title="Salvar arquivo de saída",
        defaultextension=".eng",
        filetypes=(("Arquivos de motor (.eng)", "*.eng"), ("Todos os arquivos", "*.*"))
    )
    if not caminho_saida:
        return

    try:
        result = process_data(dados)

        nome = entrada_nome.get()
        diametro = entrada_diametro.get()
        comprimento = entrada_comprimento.get()
        delays = entrada_delays.get()
        massaprop = entrada_massaprop.get()
        massatotal = entrada_massatotal.get()
        fabricante = entrada_fabricante.get()

        with open(caminho_saida, 'w') as output_file:
            output_file.write(f"{nome} {diametro} {comprimento} "
                              f"{delays} {massaprop} {massatotal} "
                              f" {fabricante}\n")
            for line in result:
                output_file.write(line + '\n')

        messagebox.showinfo("Sucesso", f"Os dados foram salvos em '{caminho_saida}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar os dados:\n{e}")

# Configuração da interface gráfica
ctk.set_appearance_mode("dark")
janela = ctk.CTk()
janela.title("Processador de Dados de Motor")
janela.geometry("900x500")

entrada_nome = ctk.StringVar()
entrada_diametro = ctk.StringVar()
entrada_comprimento = ctk.StringVar()
entrada_delays = ctk.StringVar()
entrada_massaprop = ctk.StringVar()
entrada_massatotal = ctk.StringVar()
entrada_fabricante = ctk.StringVar()

# Dividindo a janela em dois frames
frame_esquerdo = ctk.CTkFrame(janela, width=400)
frame_esquerdo.pack(side="left", fill="y", padx=10, pady=10)

frame_direito = ctk.CTkFrame(janela, width=500)
frame_direito.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Widgets no frame esquerdo
ctk.CTkLabel(frame_esquerdo, text="Parâmetros do motor:", font=("Arial", 14)).pack(pady=10)

# Adicionando rótulos e entradas com nomes ao lado
def criar_linha_parametro(frame, texto, variavel):
    linha = ctk.CTkFrame(frame)
    linha.pack(fill="x", pady=5)
    ctk.CTkLabel(linha, text=texto, width=100, anchor="w").pack(side="left", padx=5)
    ctk.CTkEntry(linha, textvariable=variavel, width=200).pack(side="right", padx=5)

criar_linha_parametro(frame_esquerdo, "Nome:", entrada_nome)
criar_linha_parametro(frame_esquerdo, "Diâmetro(mm):", entrada_diametro)
criar_linha_parametro(frame_esquerdo, "Comprimento(mm):", entrada_comprimento)
criar_linha_parametro(frame_esquerdo, "Delays(P caso não exista):", entrada_delays)
criar_linha_parametro(frame_esquerdo, "Massa Propelente(kg):", entrada_massaprop)
criar_linha_parametro(frame_esquerdo, "Massa Total(kg):", entrada_massatotal)
criar_linha_parametro(frame_esquerdo, "Fabricante:", entrada_fabricante)

ctk.CTkButton(frame_esquerdo, text="Processar e Salvar", command=salvar_arquivo).pack(pady=20)

# Widgets no frame direito
ctk.CTkLabel(frame_direito, text="Insira os dados abaixo:", font=("Arial", 14)).pack(pady=10)
caixa_texto = ctk.CTkTextbox(frame_direito, width=450, height=400, wrap="word")
caixa_texto.pack(padx=10, pady=10, fill="both", expand=True)

# Executa a interface
janela.mainloop()
