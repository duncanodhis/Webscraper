import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import json

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")
        self.create_widgets()

    def create_widgets(self):
        # URL input
        self.url_label = tk.Label(self.root, text="Enter URLs (comma-separated):")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(self.root, width=80)
        self.url_entry.pack(pady=5)

        # Scrape button
        self.scrape_button = tk.Button(self.root, text="Scrape", command=self.scrape_urls)
        self.scrape_button.pack(pady=10)

        # Frame for Text and Scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Result display
        self.result_text = tk.Text(self.frame, wrap=tk.WORD, height=20, width=80, yscrollcommand=self.scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_file)
        self.save_button.pack(pady=10)

    def scrape_urls(self):
        urls = self.url_entry.get().split(',')
        if not urls:
            messagebox.showwarning("Input Error", "Please enter some URLs.")
            return

        try:
            response = requests.post("http://127.0.0.1:8000/scrape", json={"urls": urls})
            response.raise_for_status()
            data = response.json()
            self.display_results(data)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Request Error", str(e))

    def display_results(self, data):
        self.result_text.delete(1.0, tk.END)
        docs = data.get("docs", [])
        for doc in docs:
            self.result_text.insert(tk.END, doc["page_content"] + "\n\n")

    def save_file(self):
        content = self.result_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Save Error", "No content to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
