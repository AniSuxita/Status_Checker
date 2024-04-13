import tkinter as tk
from tkinter import filedialog, messagebox
import asyncio
import scraping
import threading
import queue


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Webpage Status Checker")
        self.root.geometry("750x250")
        self.root.iconbitmap('.venv/status-checker-icon.ico')  # Set the path to your icon file

        # Styling
        self.root.config(bg="#031c71")

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.main_frame.pack(pady=20)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Check webpage statuses", font=("Inter", 20, "bold"), bg="#e6e6e6", fg="#140c28")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # URL Label and Entry
        self.url_label = tk.Label(self.main_frame, text="Sitemap URL", font=("Inter", 14), bg="#e6e6e6")
        self.url_label.grid(row=1, column=0, padx=10, sticky="w")
        self.url_entry = tk.Entry(self.main_frame, width=50, font=("Inter", 12), bg="#f5f5f5")
        self.url_entry.grid(row=1, column=1, padx=10, pady=10)

        # Path Label and Entry
        self.path_label = tk.Label(self.main_frame, text="Path", font=("Inter", 14), bg="#e6e6e6")
        self.path_label.grid(row=2, column=0, padx=10, sticky="w")
        self.path_entry = tk.Entry(self.main_frame, width=50, font=("Inter", 12), bg="#f5f5f5")
        self.path_entry.grid(row=2, column=1, padx=10, pady=10)

        # Browse Button
        self.browse_button = tk.Button(self.main_frame, text="BROWSE", font=("Inter", 12, "bold"), bg="#7284e0", fg="#fff", command=self.browse_button_clicked)
        self.browse_button.grid(row=2, column=2, padx=10, pady=10)

        # Start Button
        self.start_button = tk.Button(self.main_frame, text="START", font=("Inter", 12, "bold"), bg="#7284e0", fg="#fff", command=self.start_button_clicked)
        self.start_button.grid(row=3, column=1, padx=10, pady=20)

        self.queue = queue.Queue()
        self.loop = None

    def browse_button_clicked(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, save_path)

    def start_button_clicked(self):
        url = self.url_entry.get()
        save_path = self.path_entry.get()
        self.queue.put((url, save_path))

    async def run_asyncio(self):
        while True:
            try:
                url, save_path = self.queue.get_nowait()
                messagebox.showinfo("Loading", "Fetching webpage statuses...")
                await scraping.fetch_all_webpage_statuses(url, save_path)
                messagebox.showinfo("Success", "Webpage statuses fetched and saved successfully!")
            except queue.Empty:
                pass
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            await asyncio.sleep(0.1)

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_asyncio())


def create_gui():
    root = tk.Tk()
    app = App(root)
    threading.Thread(target=app.run, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
