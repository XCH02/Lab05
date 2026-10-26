from xml.sax import handler

import flet as ft
from flet.controls.core.canvas import color

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    tipo= ft.TextField(label = "Tipo")
    marca = ft.TextField(label = "Marca")
    anno = ft.TextField(label = "Anno")


    def handler_minus(e):
        valore_corrente=float(buttonText.value) #da cui prendo il valore corrente del testo bottone
        valore_corrente= valore_corrente - 1
        #aggiorno il valore
        buttonText.value = valore_corrente
        buttonText.update()


    def handler_plus(e):
        valore_corrente=float(buttonText.value)
        valore_corrente= valore_corrente + 1
        #aggiorno il valore
        buttonText.value = valore_corrente
        buttonText.update()



    myBtnMinus = ft.IconButton(icon = ft.Icons.REMOVE,
                               icon_size = 30,
                               icon_color = "red",
                               on_click = handler_minus)

    myBtnPlus = ft.IconButton(icon = ft.Icons.ADD,
                              icon_color = "green",
                              icon_size = 30,
                              on_click = handler_plus)

    buttonText= ft.TextField(value= 0,
                             disabled = True,
                             width = 120,
                             text_size = 20,
                             text_align = ft.TextAlign.CENTER)


    riga=ft.Row([tipo, marca, anno,myBtnMinus,buttonText,myBtnPlus],alignment=ft.MainAxisAlignment.CENTER)




    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    # Inserisco qui l'evento per la gestione
    def aggiungi_strumento(e):

        tipo_valido= tipo.value.strip()
        marca_valido=marca.value.strip()
        anno_valido=anno.value.strip()
        contatore=buttonText.value

        #gestione dell'erroe nel caso non è valido ostrare un erroe
        if not anno_valido.isdigit():
            alert.show_alert(f"Errore: inserisci valori numerici validi per anno")

        deposito.aggiungi_strumento(tipo_valido, marca_valido, anno_valido,contatore)
        #pulisco i campi per poi invocare la fuznione aggiornare la nuova lista
        tipo.value = ""
        marca.value = ""
        anno.value = ""
        buttonText.value = 0
        #qui faccio il refresh e mi aggiorna la nuova lista
        aggiorna_lista_strumenti()
        page.update()




    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    #inserisco qui il pulsante
    button_aggiungi_strumento=ft.Button(content="Aggiungi strumento", on_click=aggiungi_strumento)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento",size=20),
        riga,
        button_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
