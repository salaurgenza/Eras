import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

BASE_PATH = Path.home() / "Desktop" / "MAXI"
BASE_PATH.mkdir(parents=True, exist_ok=True)

allegati_files = []

def allega_file():
    global allegati_files
    files = filedialog.askopenfilenames(title="Seleziona file da allegare")
    destinazione = BASE_PATH / "note_allegate"
    destinazione.mkdir(exist_ok=True)
    for file in files:
        try:
            src_path = Path(file)
            dst_path = destinazione / src_path.name
            with open(src_path, "rb") as fsrc, open(dst_path, "wb") as fdst:
                fdst.write(fsrc.read())
            allegati_files.append(dst_path)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'allegato: {e}")
    if files:
        messagebox.showinfo("File Allegati", f"{len(files)} file allegati correttamente.")

def invia_email(stati, nome, cognome, cf, mail, telefono, destinatario, note, allegati):
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 465

    mittente = os.getenv("EMAIL_USER", "pepestefano@yahoo.it")
    password = os.getenv("EMAIL_PASS", "sfyrpsjkhqogzxrp")

    try:
        subject = f"Notifica stato paziente: {', '.join(stati).upper()} - {nome} {cognome}"
        msg = MIMEMultipart()
        msg["From"] = mittente
        msg["To"] = destinatario
        msg["Subject"] = subject

        corpo = f"""⚠️ Stati aggiornati: {', '.join(stati).upper()}.

Paziente: {nome} {cognome}
Codice Fiscale: {cf}
Email: {mail}
Telefono: {telefono}

Note:
{note}

Prendere nota e procedere secondo le procedure."""
        msg.attach(MIMEText(corpo, "plain"))

        for file_path in allegati:
            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_path.name}")
            msg.attach(part)

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(mittente, password)
            server.sendmail(mittente, destinatario, msg.as_string())
        messagebox.showinfo("Email inviata", "✅ Email inviata con successo!")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'invio dell'email: {e}")

def gestisci_paziente():
    nome = entry_nome.get().strip()
    cognome = entry_cognome.get().strip()
    cf = entry_cf.get().strip()
    mail = entry_mail.get().strip()
    telefono = entry_telefono.get().strip()
    destinatario = entry_destinatario.get().strip()

    stati_selezionati = []
    if var_accoglienza.get():
        stati_selezionati.append("Accoglienza")
    if var_prericovero.get():
        stati_selezionati.append("Pre-ricovero")
    if var_ricovero.get():
        stati_selezionati.append("Ricovero")
    if var_intervento.get():
        stati_selezionati.append("Intervento")
    if var_dimesso.get():
        stati_selezionati.append("Dimesso")
    if var_trasferito.get():
        stati_selezionati.append("Trasferito")

    note = note_text.get("1.0", "end").strip()

    if not nome or not cognome:
        messagebox.showwarning("Attenzione", "Inserisci nome e cognome!")
        return
    if not stati_selezionati:
        messagebox.showwarning("Attenzione", "Seleziona almeno uno stato!")
        return
    if not destinatario:
        messagebox.showwarning("Attenzione", "Inserisci il destinatario dell'email!")
        return

    invia_email(stati_selezionati, nome, cognome, cf, mail, telefono, destinatario, note, allegati_files)

def crea_finestra():
    global note_text, entry_nome, entry_cognome, entry_cf, entry_mail, entry_telefono, entry_destinatario
    global var_accoglienza, var_prericovero, var_ricovero, var_intervento, var_dimesso, var_trasferito

    root = tk.Tk()
    root.title("Notifica Paziente")

    # Nome e Cognome
    tk.Label(root, text="Nome:").grid(row=0, column=0, sticky="e")
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1)

    tk.Label(root, text="Cognome:").grid(row=1, column=0, sticky="e")
    entry_cognome = tk.Entry(root)
    entry_cognome.grid(row=1, column=1)

    # Codice Fiscale
    tk.Label(root, text="Codice Fiscale:").grid(row=2, column=0, sticky="e")
    entry_cf = tk.Entry(root)
    entry_cf.grid(row=2, column=1)

    # Email
    tk.Label(root, text="Email:").grid(row=3, column=0, sticky="e")
    entry_mail = tk.Entry(root)
    entry_mail.grid(row=3, column=1)

    # Telefono
    tk.Label(root, text="Telefono:").grid(row=4, column=0, sticky="e")
    entry_telefono = tk.Entry(root)
    entry_telefono.grid(row=4, column=1)

    # Destinatario Email
    tk.Label(root, text="Destinatario Email:").grid(row=5, column=0, sticky="e")
    entry_destinatario = tk.Entry(root)
    entry_destinatario.grid(row=5, column=1)
    entry_destinatario.insert(0, "ofthalmic.nurse.operation.room@gmail.com")

    # Checkbox stati
    var_accoglienza = tk.BooleanVar()
    var_prericovero = tk.BooleanVar()
    var_ricovero = tk.BooleanVar()
    var_intervento = tk.BooleanVar()
    var_dimesso = tk.BooleanVar()
    var_trasferito = tk.BooleanVar()

    tk.Checkbutton(root, text="Accoglienza", variable=var_accoglienza).grid(row=6, column=1, sticky="w")
    tk.Checkbutton(root, text="Pre-ricovero", variable=var_prericovero).grid(row=7, column=1, sticky="w")
    tk.Checkbutton(root, text="Ricovero", variable=var_ricovero).grid(row=8, column=1, sticky="w")
    tk.Checkbutton(root, text="Intervento", variable=var_intervento).grid(row=9, column=1, sticky="w")
    tk.Checkbutton(root, text="Dimesso", variable=var_dimesso).grid(row=10, column=1, sticky="w")
    tk.Checkbutton(root, text="Trasferito", variable=var_trasferito).grid(row=11, column=1, sticky="w")

    # Note
    tk.Label(root, text="Note:").grid(row=12, column=0, sticky="ne")
    note_text = tk.Text(root, height=5, width=40)
    note_text.grid(row=12, column=1, pady=5)

    # Bottone allega file
    tk.Button(root, text="📌 Allega File", command=allega_file).grid(row=13, column=1, sticky="w", pady=5)

    # Bottone invia
    tk.Button(root, text="Invia Notifica", command=gestisci_paziente).grid(row=14, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    crea_finestra()
