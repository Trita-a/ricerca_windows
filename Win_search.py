import os
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import threading
import queue
from datetime import datetime
import getpass
import zipfile
from ttkbootstrap.dialogs import Querybox

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search Tool")
        self.root.geometry("800x750")
        
        # Variabili
        self.search_path = ttk.StringVar()
        self.keywords = ttk.StringVar()
        self.search_results = []
        self.search_files = ttk.BooleanVar(value=True)
        self.search_folders = ttk.BooleanVar(value=True)
        self.is_searching = False
        self.progress_queue = queue.Queue()
        
        # Info utente e datetime
        self.current_user = getpass.getuser()
        self.datetime_var = ttk.StringVar()
        self.update_datetime()
        
        self.create_widgets()
        
    def update_datetime(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.datetime_var.set(f"Data: {current_time} | Utente: {self.current_user}")
        self.root.after(1000, self.update_datetime)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.search_path.set(directory)
            
    def start_search(self):
        # Pulisci risultati precedenti
        for item in self.results_list.get_children():
            self.results_list.delete(item)
        
        if not self.search_path.get() or not self.keywords.get():
            messagebox.showerror("Errore", "Inserisci directory e parole chiave")
            return
        
        self.is_searching = True
        self.search_button["state"] = "disabled"
        self.progress_bar["value"] = 0
        self.status_label["text"] = "Conteggio file in corso..."
        
        # Avvia la ricerca in un thread separato
        search_thread = threading.Thread(target=self.search_files_and_folders)
        search_thread.start()
        
        # Avvia l'aggiornamento della progress bar
        self.update_progress()

    def update_progress(self):
        if self.is_searching:
            try:
                while True:
                    progress_type, value = self.progress_queue.get_nowait()
                    if progress_type == "progress":
                        self.progress_bar["value"] = value
                    elif progress_type == "status":
                        self.status_label["text"] = value
                    elif progress_type == "complete":
                        self.is_searching = False
                        self.search_button["state"] = "normal"
                        self.status_label["text"] = "Ricerca completata!"
                        self.progress_bar["value"] = 100
                        return
            except queue.Empty:
                pass
            
            self.root.after(100, self.update_progress)
        
    def create_widgets(self):
        # Frame principale che conterrà tutto tranne la barra di stato
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Frame principale per il contenuto
        main_frame = ttk.Frame(main_container, padding="10")
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Sezione selezione directory
        path_frame = ttk.LabelFrame(main_frame, text="Directory di ricerca", padding="5")
        path_frame.pack(fill=X, pady=5)
        
        ttk.Entry(path_frame, textvariable=self.search_path).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(path_frame, text="Sfoglia", command=self.browse_directory).pack(side=LEFT, padx=5)
        
        # Sezione keywords
        keyword_frame = ttk.LabelFrame(main_frame, text="Parole chiave", padding="5")
        keyword_frame.pack(fill=X, pady=5)
        
        ttk.Entry(keyword_frame, textvariable=self.keywords).pack(fill=X, padx=5)
        
        # Opzioni di ricerca
        options_frame = ttk.LabelFrame(main_frame, text="Opzioni di ricerca", padding="5")
        options_frame.pack(fill=X, pady=5)
        
        ttk.Checkbutton(options_frame, text="Cerca file", variable=self.search_files).pack(side=LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Cerca cartelle", variable=self.search_folders).pack(side=LEFT, padx=5)
        
        # Pulsante di ricerca
        self.search_button = ttk.Button(main_frame, text="Cerca", 
                                      command=self.start_search, 
                                      style="primary.TButton")
        self.search_button.pack(pady=5)
        
        # Area risultati
        results_frame = ttk.LabelFrame(main_frame, text="Risultati", padding="5")
        results_frame.pack(fill=BOTH, expand=YES, pady=5)
        
        # Frame per i pulsanti di azione
        action_buttons_frame = ttk.Frame(results_frame)
        action_buttons_frame.pack(fill=X, pady=(0, 5))
        
        # Pulsanti per la selezione
        ttk.Button(action_buttons_frame, text="Seleziona tutto", 
                  command=self.select_all).pack(side=LEFT, padx=2)
        ttk.Button(action_buttons_frame, text="Deseleziona tutto", 
                  command=self.deselect_all).pack(side=LEFT, padx=2)
        ttk.Button(action_buttons_frame, text="Inverti selezione", 
                  command=self.invert_selection).pack(side=LEFT, padx=2)
        
        # Scrollbar per la lista risultati
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.results_list = ttk.Treeview(results_frame, selectmode="extended", 
                                       columns=("type", "path"),
                                       show="headings")
        self.results_list.heading("type", text="Tipo")
        self.results_list.heading("path", text="Percorso")
        self.results_list.column("type", width=100)
        self.results_list.column("path", width=600)
        
        self.results_list.pack(fill=BOTH, expand=YES)
        
        scrollbar.config(command=self.results_list.yview)
        self.results_list.config(yscrollcommand=scrollbar.set)
        
        # Frame per i pulsanti di azione principali
        main_buttons_frame = ttk.Frame(main_frame)
        main_buttons_frame.pack(fill=X, pady=5)
        
        # Pulsanti copia e comprimi
        self.copy_button = ttk.Button(main_buttons_frame, text="Copia selezionati", 
                                    command=self.copy_selected, 
                                    style="secondary.TButton")
        self.copy_button.pack(side=LEFT, padx=5)
        
        self.compress_button = ttk.Button(main_buttons_frame, text="Comprimi selezionati", 
                                        command=self.compress_selected, 
                                        style="info.TButton")
        self.compress_button.pack(side=LEFT, padx=5)
        
        # Frame della barra di stato (in basso)
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=X, side=BOTTOM, pady=2)
        
        # Frame info (sinistra)
        info_frame = ttk.Frame(status_frame)
        info_frame.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        # Status label (in basso a sinistra)
        self.status_label = ttk.Label(info_frame, text="In attesa...", justify=LEFT)
        self.status_label.pack(side=LEFT, padx=5)
        
        # DateTime e User label (in basso a destra)
        ttk.Label(status_frame, textvariable=self.datetime_var).pack(side=RIGHT, padx=5)
        
        # Progress bar (sopra la barra di stato)
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill=X, side=BOTTOM, pady=(0, 2))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=200)
        self.progress_bar.pack(fill=X, padx=5)

    def select_all(self):
        self.results_list.selection_set(self.results_list.get_children())
        
    def deselect_all(self):
        self.results_list.selection_remove(self.results_list.get_children())
        
    def invert_selection(self):
        all_items = self.results_list.get_children()
        selected_items = self.results_list.selection()
        self.results_list.selection_remove(selected_items)
        to_select = set(all_items) - set(selected_items)
        for item in to_select:
            self.results_list.selection_add(item)

    def compress_selected(self):
        selected_items = self.results_list.selection()
        if not selected_items:
            messagebox.showwarning("Attenzione", "Seleziona almeno un elemento da comprimere")
            return
            
        zip_name = Querybox.get_string(
            prompt="Inserisci il nome del file ZIP (senza estensione):",
            title="Nome file ZIP",
            initialvalue="archivio"
        )
        
        if not zip_name:
            return
            
        zip_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            initialfile=f"{zip_name}.zip",
            filetypes=[("ZIP files", "*.zip")],
            title="Salva file ZIP"
        )
        
        if not zip_path:
            return
            
        # Raccogli tutti i file delle cartelle selezionate
        files_in_folders = set()
        folder_paths = []
        single_files = []
        
        # Prima fase: raccogli informazioni su cartelle e file
        for item in selected_items:
            values = self.results_list.item(item)['values']
            item_type, source_path = values
            
            if item_type == "Cartella":
                folder_paths.append(source_path)
                # Raccogli tutti i file nelle cartelle selezionate
                for root, _, files in os.walk(source_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        files_in_folders.add(os.path.abspath(full_path))
            else:
                single_files.append(source_path)
        
        # Filtra i file singoli che sono già presenti nelle cartelle
        filtered_single_files = [f for f in single_files if os.path.abspath(f) not in files_in_folders]
        
        total_items = len(folder_paths) + len(filtered_single_files)
        processed = 0
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Prima comprimi le cartelle
                for folder_path in folder_paths:
                    base_folder = os.path.basename(folder_path)
                    for root, _, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Mantieni la struttura delle cartelle nel zip
                            rel_path = os.path.relpath(file_path, os.path.dirname(folder_path))
                            zipf.write(file_path, rel_path)
                    
                    processed += 1
                    progress = (processed / total_items) * 100
                    self.progress_bar["value"] = progress
                    self.status_label["text"] = f"Compressi {processed} di {total_items} elementi"
                    self.root.update()
                
                # Poi comprimi i file singoli (solo quelli non già presenti nelle cartelle)
                for file_path in filtered_single_files:
                    if os.path.exists(file_path):  # Verifica che il file esista ancora
                        zipf.write(file_path, os.path.basename(file_path))
                        
                    processed += 1
                    progress = (processed / total_items) * 100
                    self.progress_bar["value"] = progress
                    self.status_label["text"] = f"Compressi {processed} di {total_items} elementi"
                    self.root.update()
            
            # Prepara il messaggio di completamento
            skipped_files = len(single_files) - len(filtered_single_files)
            message = f"Compressione completata!\nFile salvato in: {zip_path}"
            if skipped_files > 0:
                message += f"\n{skipped_files} file saltati perché già presenti nelle cartelle"
                
            messagebox.showinfo("Completato", message)
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la compressione: {str(e)}")
            
        finally:
            self.progress_bar["value"] = 0
            self.status_label["text"] = "In attesa..."

    def copy_selected(self):
        selected_items = self.results_list.selection()
        if not selected_items:
            messagebox.showwarning("Attenzione", "Seleziona almeno un elemento da copiare")
            return
            
        dest_dir = filedialog.askdirectory(title="Seleziona directory di destinazione")
        if not dest_dir:
            return
            
        total_items = len(selected_items)
        copied = 0
        errors = 0
        
        for i, item in enumerate(selected_items):
            values = self.results_list.item(item)['values']
            item_type, source_path = values
            
            try:
                dest_path = os.path.join(dest_dir, os.path.basename(source_path))
                
                if item_type == "File":
                    shutil.copy2(source_path, dest_path)
                else:  # Cartella
                    shutil.copytree(source_path, dest_path)
                copied += 1
                
            except Exception as e:
                errors += 1
                print(f"Errore durante la copia di {source_path}: {str(e)}")
            
            # Aggiorna la progress bar
            progress = ((i + 1) / total_items) * 100
            self.progress_bar["value"] = progress
            self.status_label["text"] = f"Copiati {i + 1} di {total_items} elementi"
            self.root.update()
                
        message = f"Copia completata.\nCopiati con successo: {copied}"
        if errors > 0:
            message += f"\nErrori: {errors}"
            
        self.status_label["text"] = "Copia completata"
        messagebox.showinfo("Completato", message)

    def search_files_and_folders(self):
        keywords = [k.strip().lower() for k in self.keywords.get().split()]
        self.search_results = []
        
        # Prima conta il numero totale di elementi da processare
        total_items = 0
        for _, dirs, files in os.walk(self.search_path.get()):
            if self.search_folders.get():
                total_items += len(dirs)
            if self.search_files.get():
                total_items += len(files)
        
        processed_items = 0
        folders_results = []
        files_results = []
        
        for root, dirs, files in os.walk(self.search_path.get()):
            # Cerca nelle cartelle
            if self.search_folders.get():
                for dir_name in dirs:
                    if any(keyword in dir_name.lower() for keyword in keywords):
                        full_path = os.path.join(root, dir_name)
                        folders_results.append(("Cartella", full_path))
                    
                    processed_items += 1
                    progress = (processed_items / total_items) * 100
                    self.progress_queue.put(("progress", progress))
                    self.progress_queue.put(("status", f"Processati {processed_items} di {total_items} elementi"))
                        
            # Cerca nei file
            if self.search_files.get():
                for file_name in files:
                    if any(keyword in file_name.lower() for keyword in keywords):
                        full_path = os.path.join(root, file_name)
                        files_results.append(("File", full_path))
                    
                    processed_items += 1
                    progress = (processed_items / total_items) * 100
                    self.progress_queue.put(("progress", progress))
                    self.progress_queue.put(("status", f"Processati {processed_items} di {total_items} elementi"))
        
        # Ordina i risultati (prima cartelle, poi file)
        folders_results.sort(key=lambda x: x[1].lower())
        files_results.sort(key=lambda x: x[1].lower())
        self.search_results = folders_results + files_results
        
        # Aggiorna la lista dei risultati
        self.root.after(0, self.update_results_list)
        
        self.progress_queue.put(("complete", None))
        
        if not self.search_results:
            self.root.after(0, lambda: messagebox.showinfo("Risultati", "Nessun risultato trovato"))

    def update_results_list(self):
        # Pulisci la lista
        for item in self.results_list.get_children():
            self.results_list.delete(item)
        
        # Inserisci i risultati ordinati
        for item_type, path in self.search_results:
            self.results_list.insert("", END, values=(item_type, path))

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = FileSearchApp(root)
    root.mainloop()
