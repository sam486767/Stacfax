import sys
import subprocess
import json
import tkinter as tk
import urllib.request

# --- Base URL for your GitHub Pages content ---
BASE_URL = "https://sam486767.github.io/Stacfax/pages/"

class TeletextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teletext Viewer")

        # Title
        self.title_label = tk.Label(root, text="Teletext", font=("Courier", 16, "bold"))
        self.title_label.pack(pady=5)

        # Main text area (monospace to mimic teletext)
        self.text_area = tk.Text(root, width=40, height=20, font=("Courier", 12))
        self.text_area.pack(pady=5)

        # Page entry + load button
        controls = tk.Frame(root)
        controls.pack(pady=5)

        self.page_entry = tk.Entry(controls, width=6, font=("Courier", 12))
        self.page_entry.grid(row=0, column=0, padx=5)

        self.load_button = tk.Button(controls, text="Load", command=self.load_page)
        self.load_button.grid(row=0, column=1, padx=5)

        self.prev_button = tk.Button(controls, text="◀ Prev", command=self.prev_page)
        self.prev_button.grid(row=0, column=2, padx=5)

        self.next_button = tk.Button(controls, text="Next ▶", command=self.next_page)
        self.next_button.grid(row=0, column=3, padx=5)

        # Start at page 100
        self.current_page = 100
        self.show_page(self.current_page)

    def fetch_page(self, page_number):
        url = f"{BASE_URL}{page_number}.json"
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode("utf-8")
                return json.loads(data)
        except Exception as e:

            print(f"Error fetching page {page_number} from {url}: {e}")
            return {"title": "Error", "lines": [f"Could not load page {page_number}.", str(e)]}

    def show_page(self, page_number):
        page = self.fetch_page(page_number)
        self.title_label.config(text=f"{page.get('title', 'Untitled')} (Page {page_number})")

        self.text_area.delete("1.0", tk.END)
        for line in page.get("lines", []):
            self.text_area.insert(tk.END, line + "\n")

    def load_page(self):
        try:
            page_number = int(self.page_entry.get())
            self.current_page = page_number
            self.show_page(page_number)
        except ValueError:
            self.text_area.insert(tk.END, "\nInvalid page number.\n")

    def prev_page(self):
        self.current_page -= 1
        self.show_page(self.current_page)

    def next_page(self):
        self.current_page += 1
        self.show_page(self.current_page)

if __name__ == "__main__":
    root = tk.Tk()
    app = TeletextApp(root)
    root.mainloop()
