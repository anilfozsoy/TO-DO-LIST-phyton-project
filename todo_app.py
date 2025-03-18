import json
import os
import tkinter as tk
from tkinter import messagebox
import time
import threading

TODO_FILE = "todo.json"
DARK_MODE = False  # Başlangıçta açık mod

# Görevleri JSON dosyasına kaydetme
def save_tasks():
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Görevleri JSON dosyasından yükleme
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []

# Görevleri ekranda güncelleme
def update_listbox():
    listbox.delete(0, tk.END)
    for idx, task in enumerate(tasks):
        status = "✅ " if task["done"] else "❌ "
        priority = task["priority"]

        # Önceliğe göre renklendirme
        if priority == "Yüksek":
            color = "red"
        elif priority == "Orta":
            color = "orange"
        else:
            color = "green"

        listbox.insert(tk.END, f"{status}{task['task']} ({priority})")
        listbox.itemconfig(idx, {'fg': color})

# Görev ekleme fonksiyonu
def add_task():
    task = entry.get().strip()
    priority = priority_var.get()

    if task:
        tasks.append({"task": task, "done": False, "priority": priority})
        save_tasks()
        update_listbox()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir görev girin!")

# Görevi tamamlandı olarak işaretleme
def complete_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        tasks[index]["done"] = True
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("Uyarı", "Tamamlanan görevi seçin!")

# Görev silme fonksiyonu
def delete_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        del tasks[index]
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("Uyarı", "Silmek için bir görev seçin!")

# Koyu mod aç/kapat
def toggle_theme():
    global DARK_MODE
    DARK_MODE = not DARK_MODE
    if DARK_MODE:
        root.configure(bg="#2E2E2E")
        listbox.configure(bg="#1E1E1E", fg="white")
        theme_button.configure(text="🌞 Açık Mod", bg="gray")
    else:
        root.configure(bg="#f7f7f7")
        listbox.configure(bg="white", fg="black")
        theme_button.configure(text="🌙 Koyu Mod", bg="black", fg="white")

# Hatırlatma fonksiyonu (Belirtilen süre sonra mesaj verir)
def set_reminder():
    reminder_time = int(reminder_entry.get())
    reminder_message = reminder_task_entry.get()

    if reminder_message and reminder_time > 0:
        messagebox.showinfo("Hatırlatma Ayarlandı", f"{reminder_time} saniye sonra hatırlatma yapılacak!")

        def reminder():
            time.sleep(reminder_time)
            messagebox.showinfo("⏰ Hatırlatma!", f"Unutmayın: {reminder_message}")

        threading.Thread(target=reminder).start()
    else:
        messagebox.showwarning("Uyarı", "Lütfen geçerli bir süre ve görev girin!")

# Pencere kapanırken görevleri kaydet
def on_closing():
    save_tasks()
    root.destroy()

# 🎨 Arayüz Tasarımı
root = tk.Tk()
root.title("📋 To-Do List Uygulaması")
root.geometry("400x550")  # Boyut
root.configure(bg="#f7f7f7")

# Görevleri yükle
tasks = load_tasks()

# Üst Çerçeve (Başlık ve Giriş)
frame = tk.Frame(root, bg="#f7f7f7")
frame.pack(pady=10)

entry = tk.Entry(frame, width=30, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)

priority_var = tk.StringVar(value="Düşük")
priority_menu = tk.OptionMenu(frame, priority_var, "Düşük", "Orta", "Yüksek")
priority_menu.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="➕ Ekle", command=add_task, bg="#007bff", fg="white", font=("Arial", 12))
add_button.pack(side=tk.RIGHT)

# Liste Kutusu (Görevleri Göster)
listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12), bg="white", fg="black")
listbox.pack(pady=10)

update_listbox()  # Başlangıçta listeyi güncelle

# Butonlar
button_frame = tk.Frame(root, bg="#f7f7f7")
button_frame.pack(pady=10)

complete_button = tk.Button(button_frame, text="✔️ Tamamlandı", command=complete_task, bg="#28a745", fg="white", font=("Arial", 12))
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="🗑️ Sil", command=delete_task, bg="#dc3545", fg="white", font=("Arial", 12))
delete_button.pack(side=tk.RIGHT, padx=5)

# 🌙 Koyu Mod Butonu
theme_button = tk.Button(root, text="🌙 Koyu Mod", command=toggle_theme, bg="black", fg="white", font=("Arial", 12))
theme_button.pack(pady=5)

# ⏰ Hatırlatma Sistemi
reminder_frame = tk.Frame(root, bg="#f7f7f7")
reminder_frame.pack(pady=10)

reminder_task_entry = tk.Entry(reminder_frame, width=25, font=("Arial", 12))
reminder_task_entry.pack(side=tk.LEFT, padx=5)

reminder_entry = tk.Entry(reminder_frame, width=5, font=("Arial", 12))
reminder_entry.pack(side=tk.LEFT, padx=5)

reminder_label = tk.Label(reminder_frame, text="saniye sonra", bg="#f7f7f7", font=("Arial", 10))
reminder_label.pack(side=tk.LEFT, padx=5)

reminder_button = tk.Button(reminder_frame, text="⏰ Hatırlat", command=set_reminder, bg="#ff9800", fg="white", font=("Arial", 12))
reminder_button.pack(side=tk.RIGHT, padx=5)

# Pencere kapatılınca verileri kaydet
root.protocol("WM_DELETE_WINDOW", on_closing)

# Tkinter Ana Döngüsü
root.mainloop()
