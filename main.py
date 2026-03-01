import tkinter as tk
from tkinter import messagebox
import requests
import base64

# 1. የሊንክ ምርመራ
def check_link():
    url = link_entry.get().strip()
    api_key = "b5a441cba28b200c154f64b3a96fb18f315846391178b0917ae6af3bf65607d0"
    if not url.startswith("http"):
        messagebox.showwarning("Net Warden", "ሊንኩን በ http:// ወይም https:// ይጀምሩ!")
        return
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {"x-apikey": api_key}
        resp = requests.get(api_url, headers=headers)
        if resp.status_code == 200:
            stats = resp.json().get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
            malicious = stats.get('malicious', 0)
            res = "❌ SCAM / DANGEROUS!" if malicious > 0 else "✅ SAFE / LEGIT"
            messagebox.showinfo("Link Security", res)
        else: messagebox.showerror("Error", "ሊንኩን መፈተሽ አልተቻለም")
    except: messagebox.showerror("Error", "የኢንተርኔት ግንኙነት የለም!")

# 2. የአይፒ መከታተያ
def check_ip():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showwarning("Net Warden", "እባክዎ IP ያስገቡ!")
        return
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}")
        data = resp.json()
        if data['status'] == 'success':
            info = f"ሀገር: {data['country']}\nከተማ: {data['city']}\nISP: {data['isp']}"
            messagebox.showinfo("IP Location", info)
        else: messagebox.showerror("Error", "አይፒው አልተገኘም!")
    except: messagebox.showerror("Error", "ግንኙነት የለም!")

# 3. የ ID ምርመራ
def check_id():
    target_id = id_entry.get().strip()
    scam_ids = ["12345", "99999", "00000"]
    legit_ids = ["8115", "8116", "2026"]
    if target_id in scam_ids:
        messagebox.showerror("ID Report", f"❌ SCAM!\nመለያ {target_id} የታወቀ ሌባ ነው።")
    elif target_id in legit_ids:
        messagebox.showinfo("ID Report", f"✅ LEGIT!\nመለያ {target_id} የታመነ ነው።")
    else: messagebox.showwarning("ID Report", "🔍 UNKNOWN\nመለያው ዳታቤዝ ውስጥ የለም።")

# --- UI ገጽታ (ልክ በፎቶህ ላይ እንዳለው) ---
root = tk.Tk()
root.title("Net Warden Pro v7.6")
root.geometry("400x750")
root.configure(bg="#000000")

tk.Label(root, text="NET WARDEN", font=("Arial", 28, "bold"), fg="#00FF00", bg="#000000").pack(pady=20)

# የሊንክ ክፍል
tk.Label(root, text="SCAN LINK (Security Check)", fg="white", bg="#000000", font=("Arial", 11)).pack()
link_entry = tk.Entry(root, font=("Arial", 14), width=28, bg="#1A1A1A", fg="white", insertbackground="white")
link_entry.pack(pady=5); link_entry.insert(0, "https://")
tk.Button(root, text="CHECK LINK", font=("Arial", 10, "bold"), bg="#1B5E20", fg="white", width=25, command=check_link).pack(pady=10)

# የአይፒ ክፍል
tk.Label(root, text="TRACK IP (Location Check)", fg="white", bg="#000000", font=("Arial", 11)).pack(pady=10)
ip_entry = tk.Entry(root, font=("Arial", 14), width=28, bg="#1A1A1A", fg="white", insertbackground="white")
ip_entry.pack(pady=5)
tk.Button(root, text="TRACK IP", font=("Arial", 10, "bold"), bg="#0D47A1", fg="white", width=25, command=check_ip).pack(pady=10)

# የ ID ክፍል
tk.Label(root, text="VERIFY ID (Scam Check)", fg="white", bg="#000000", font=("Arial", 11)).pack(pady=10)
id_entry = tk.Entry(root, font=("Arial", 14), width=28, bg="#1A1A1A", fg="white", insertbackground="white")
id_entry.pack(pady=5)
tk.Button(root, text="VERIFY ID", font=("Arial", 10, "bold"), bg="#E65100", fg="white", width=25, command=check_id).pack(pady=10)

root.mainloop()
