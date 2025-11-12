import requests
import PyPDF2
import re
import tkinter
from tkinter import filedialog, messagebox, scrolledtext

def Get_text_from_PDFfiles_usingPyPDF2(in_PdfFile):
    try:
        reader = PyPDF2.PdfReader(in_PdfFile)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() or ""
        return texto
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o PDF: {e}")
        return ""

def obter_feriados(ano="2025"):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
    headers = {
        'accept': 'application/json',
        'X-CSRF-TOKEN': 'pYBqfz7tfH5NFeqA2YXNhdZIsqRCMmef6FjOTNJz'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        feriados = {f["date"]: f["localName"] for f in dados}
        return feriados
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar feriados: {e}")
        return {}

def verificar_datas():
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if not caminho_pdf:
        messagebox.showinfo("Atenção", "Nenhum arquivo selecionado.")
        return
    texto = Get_text_from_PDFfiles_usingPyPDF2(caminho_pdf)
    padrao_data = r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"
    datas_encontradas = re.findall(padrao_data, texto)
    if not datas_encontradas:
        messagebox.showinfo("Resultado", "Nenhuma data encontrada no PDF.")
        return
    datas_formatadas = []
    for d in datas_encontradas:
        if re.match(r"\d{4}-\d{2}-\d{2}", d):
            datas_formatadas.append(d)
        else:
            partes = re.split(r"[./-]", d)
            if len(partes) == 3:
                dia, mes, ano = partes
                if len(ano) == 2:
                    ano = "20" + ano
                dia = dia.zfill(2)
                mes = mes.zfill(2)
                datas_formatadas.append(f"{ano}-{mes}-{dia}")
    feriados = obter_feriados("2025")
    resultado_texto = ""
    for d in datas_formatadas:
        if d in feriados:
            resultado_texto += f"{d} → {feriados[d]}\n"
    if not resultado_texto:
        resultado_texto = "Nenhuma das datas encontradas é feriado."
    resultado_box.delete(1.0, tkinter.END)
    resultado_box.insert(tkinter.END, resultado_texto)

def Exemplo():
    global resultado_box
    root = tkinter.Tk()
    root.title("Verificador de Feriados no PDF")
    root.geometry("600x400")
    root.resizable(False, False)
    botao_pdf = tkinter.Button(root, text="Escolher PDF e Verificar Feriados", command=verificar_datas)
    botao_pdf.pack(pady=10)
    resultado_box = scrolledtext.ScrolledText(root, width=70, height=15)
    resultado_box.pack(padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    Exemplo()
