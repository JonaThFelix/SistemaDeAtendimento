import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.pdfgen import canvas
from datetime import datetime

class Atendimento:
    def __init__(self, nome, matricula, data, posto, motivo, departamento):
        self.nome = nome
        self.matricula = matricula
        self.data = data
        self.posto = posto
        self.motivo = motivo
        self.departamento = departamento
        self.data_chegada = datetime.now()

class AtendimentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atendimento")

        self.atendimentos_do_dia = []
        self.create_widgets()

    def create_widgets(self):
        # Labels e Entries para informações do atendimento
        tk.Label(self.root, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.root, width=40)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Matrícula:").grid(row=1, column=0, padx=10, pady=5)
        self.matricula_entry = tk.Entry(self.root, width=40)
        self.matricula_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Data:").grid(row=2, column=0, padx=10, pady=5)
        self.data_entry = tk.Entry(self.root, width=40)
        self.data_entry.insert(tk.END, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.data_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Posto:").grid(row=3, column=0, padx=10, pady=5)
        self.posto_entry = tk.Entry(self.root, width=40)
        self.posto_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Motivo da Visita:").grid(row=4, column=0, padx=10, pady=5)
        self.motivo_entry = tk.Entry(self.root, width=40)
        self.motivo_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Departamento:").grid(row=5, column=0, padx=10, pady=5)
        self.departamento_entry = tk.Entry(self.root, width=40)
        self.departamento_entry.grid(row=5, column=1, padx=10, pady=5)

        # Botões para adicionar/atualizar atendimento e gerar relatório
        tk.Button(self.root, text="Adicionar/Atualizar Atendimento", command=self.add_atendimento).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Gerar Relatório", command=self.generate_report).grid(row=7, column=0, columnspan=2, pady=10)

        # Lista de atendimentos do dia com barra de rolagem
        self.listbox = tk.Listbox(self.root, width=50, height=10, selectmode=tk.SINGLE)
        self.listbox.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=3, rowspan=8, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

    def add_atendimento(self):
        nome = self.nome_entry.get()
        matricula = self.matricula_entry.get()
        data = self.data_entry.get()
        posto = self.posto_entry.get()
        motivo = self.motivo_entry.get()
        departamento = self.departamento_entry.get()

        if nome and matricula and data and posto and motivo and departamento:
            atendimento = Atendimento(nome, matricula, data, posto, motivo, departamento)
            self.atendimentos_do_dia.append(atendimento)
            self.update_listbox()
            self.clear_entries()
            print("Atendimento adicionado/atualizado com sucesso.")
        else:
            print("Preencha todas as informações do atendimento.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, atendimento in enumerate(self.atendimentos_do_dia, start=1):
            self.listbox.insert(tk.END, f"Atendimento #{idx}: {atendimento.nome}")

    def clear_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.matricula_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(tk.END, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.posto_entry.delete(0, tk.END)
        self.motivo_entry.delete(0, tk.END)
        self.departamento_entry.delete(0, tk.END)

    def generate_report(self):
        folder_selected = filedialog.askdirectory(title="Escolha a pasta para salvar o relatório")
        if folder_selected:
            pdf_filename = f"{folder_selected}/relatorio_atendimentos.pdf"
            c = canvas.Canvas(pdf_filename)

            c.setFont("Helvetica", 12)
            c.drawString(100, 800, "Relatório de Atendimentos do Dia")

            y_position = 750
            for idx, atendimento in enumerate(self.atendimentos_do_dia, start=1):
                y_position -= 20
                c.drawString(100, y_position, f"Atendimento #{idx}")
                y_position -= 15
                c.drawString(120, y_position, f"Nome: {atendimento.nome}")
                y_position -= 15
                c.drawString(120, y_position, f"Matrícula: {atendimento.matricula}")
                y_position -= 15
                c.drawString(120, y_position, f"Data: {atendimento.data}")
                y_position -= 15
                c.drawString(120, y_position, f"Posto: {atendimento.posto}")
                y_position -= 15
                c.drawString(120, y_position, f"Motivo da Visita: {atendimento.motivo}")
                y_position -= 15
                c.drawString(120, y_position, f"Departamento: {atendimento.departamento}")
                y_position -= 15
                c.drawString(120, y_position, f"Data de Chegada: {atendimento.data_chegada.strftime('%Y-%m-%d %H:%M:%S')}")

            c.save()
            messagebox.showinfo("Relatório Gerado", f"Relatório gerado com sucesso: {pdf_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AtendimentoApp(root)
    root.mainloop()
