import random
import tkinter as tk
from tkinter import ttk, messagebox

# --- Data Initialization ---
DATA = {
    1: [("Real Madrid", "ESP"), ("Man City", "ENG"), ("Bayern Munich", "GER"), ("Liverpool", "ENG"), ("PSG", "FRA"), ("Inter Milan", "ITA"), ("Chelsea", "ENG"), ("Dortmund", "GER"), ("Barcelona", "ESP")],
    2: [("Arsenal", "ENG"), ("Bayer Leverkusen", "GER"), ("Atleti", "ESP"), ("Benfica", "POR"), ("Atalanta", "ITA"), ("Villarreal", "ESP"), ("Juventus", "ITA"), ("Frankfurt", "GER"), ("Club Brugge", "BEL")],
    3: [("Tottenham", "ENG"), ("PSV Eindhoven", "NED"), ("Ajax", "NED"), ("Napoli", "ITA"), ("Sporting CP", "POR"), ("Olympiacos", "GRE"), ("Slavia Prague", "CZE"), ("Bodø/Glimt", "NOR"), ("Marseille", "FRA")],
    4: [("Copenhagen", "DEN"), ("Monaco", "FRA"), ("Galatasaray", "TUR"), ("Union SG", "BEL"), ("Qarabağ", "AZE"), ("Athletic Club", "ESP"), ("Newcastle", "ENG"), ("Pafos FC", "CYP"), ("Kairat", "KAZ")]
}

ALL_CLUBS = [c for p in range(1, 5) for c, _ in DATA[p]]
CLUB_INFO = {c: {"country": n, "pot": p} for p, clubs in DATA.items() for c, n in clubs}
lookup = {c.lower(): c for c in ALL_CLUBS}

class DrawEngine:
    @staticmethod
    def is_valid(c1, c2, p2, slot, sched):
        p1 = CLUB_INFO[c1]['pot']
        opp_slot = 'A' if slot == 'H' else 'H'
        if sched[c1][p2][slot] or sched[c2][p1][opp_slot]: return False
        if CLUB_INFO[c1]['country'] == CLUB_INFO[c2]['country']: return False
        c1_counts = {}
        for p in range(1, 5):
            for s in ['H', 'A']:
                o = sched[c1][p][s]
                if o:
                    cntry = CLUB_INFO[o]['country']
                    c1_counts[cntry] = c1_counts.get(cntry, 0) + 1
        if c1_counts.get(CLUB_INFO[c2]['country'], 0) >= 2: return False
        return True

    @classmethod
    def solve(cls):
        while True:
            sched = {c: {p: {'H': None, 'A': None} for p in range(1, 5)} for c in ALL_CLUBS}
            success = True
            for team in ALL_CLUBS:
                for p_target in range(1, 5):
                    for slot in ['H', 'A']:
                        if sched[team][p_target][slot]: continue
                        candidates = [c for c, _ in DATA[p_target] if c != team and cls.is_valid(team, c, p_target, slot, sched)]
                        if not candidates:
                            success = False
                            break
                        opp = random.choice(candidates)
                        opp_p, opp_s = CLUB_INFO[team]['pot'], ('A' if slot == 'H' else 'H')
                        sched[team][p_target][slot], sched[opp][opp_p][opp_s] = opp, team
                    if not success: break
                if not success: break
            if success: return sched

class UCLDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UCL 2025/26 Draw Ceremony")
        self.root.geometry("1400x850") # Widened for sidebars
        self.root.configure(bg='#020212')
        
        self.master_sched = DrawEngine.solve()
        self.drawn_tracker = []
        self.remaining_teams = {p: [c for c, _ in DATA[p]] for p in range(1, 5)}
        
        self.setup_ui()
        self.update_sidebars()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="CHAMPIONS LEAGUE-LEAGUE PHASE DRAW", 
                 font=("Verdana", 24, "bold"), fg="#ffffff", bg="#000033", pady=15).pack(fill="x")

        # Main Layout Container (Three Columns)
        main_container = tk.Frame(self.root, bg="#020212")
        main_container.pack(expand=True, fill="both", padx=10, pady=10)

        # 1. LEFT COLUMN: COMPLETED
        self.left_col = tk.Frame(main_container, bg="#050520", width=200, padx=10)
        self.left_col.pack(side="left", fill="y", padx=5)
        tk.Label(self.left_col, text="COMPLETED", font=("Segoe UI", 12, "bold"), fg="#00ff00", bg="#050520").pack(pady=10)
        self.completed_list = tk.Text(self.left_col, bg="#020212", fg="white", font=("Segoe UI", 10), width=20, borderwidth=0)
        self.completed_list.pack(expand=True, fill="both")

        # 2. CENTER COLUMN: MAIN TABLE & CONTROLS
        center_col = tk.Frame(main_container, bg="#020212")
        center_col.pack(side="left", expand=True, fill="both", padx=5)

        # Table Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0a0a25", foreground="white", fieldbackground="#0a0a25", rowheight=45, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#00004d", foreground="white", font=("Segoe UI", 10, "bold"))
        
        columns = ("team", "p1", "p2", "p3", "p4")
        self.tree = ttk.Treeview(center_col, columns=columns, show="headings")
        self.tree.heading("team", text="TEAM")
        for i in range(1, 5):
            self.tree.heading(f"p{i}", text=f"POT {i}")
            self.tree.column(f"p{i}", width=180, anchor="center")
        self.tree.column("team", width=150, anchor="w")
        self.tree.pack(expand=True, fill="both")

        # Bottom Controls
        ctrl = tk.Frame(center_col, bg="#05051a", pady=15)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="ENTER CLUB NAME", font=("Segoe UI", 9, "bold"), fg="#8888ff", bg="#05051a").pack()
        self.entry = tk.Entry(ctrl, font=("Segoe UI", 14), width=25, bg="#101035", fg="white", insertbackground="white", justify='center')
        self.entry.pack(pady=5)
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self.process_draw())

        btn_box = tk.Frame(ctrl, bg="#05051a")
        btn_box.pack()
        tk.Button(btn_box, text="DRAW", command=self.process_draw, bg="#000066", fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(btn_box, text="DRAW ALL", command=self.draw_all, bg="#444444", fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side="left", padx=5)

        # 3. RIGHT COLUMN: REMAINING
        self.right_col = tk.Frame(main_container, bg="#050520", width=200, padx=10)
        self.right_col.pack(side="left", fill="y", padx=5)
        tk.Label(self.right_col, text="REMAINING", font=("Segoe UI", 12, "bold"), fg="#ff3333", bg="#050520").pack(pady=10)
        self.remaining_list = tk.Text(self.right_col, bg="#020212", fg="white", font=("Segoe UI", 10), width=20, borderwidth=0)
        self.remaining_list.pack(expand=True, fill="both")

    def update_sidebars(self):
        # Update Completed List
        self.completed_list.config(state="normal")
        self.completed_list.delete("1.0", tk.END)
        for team in sorted(self.drawn_tracker):
            self.completed_list.insert(tk.END, f"• {team}\n")
        self.completed_list.config(state="disabled")

        # Update Remaining List (Grouped by Pot)
        self.remaining_list.config(state="normal")
        self.remaining_list.delete("1.0", tk.END)
        for p in range(1, 5):
            rem = [c for c in self.remaining_teams[p] if c not in self.drawn_tracker]
            if rem:
                self.remaining_list.insert(tk.END, f"[POT {p}]\n", "pot_header")
                for team in sorted(rem):
                    self.remaining_list.insert(tk.END, f"  {team}\n")
                self.remaining_list.insert(tk.END, "\n")
        self.remaining_list.tag_config("pot_header", foreground="#ffff00", font=("Segoe UI", 10, "bold"))
        self.remaining_list.config(state="disabled")

    def process_draw(self):
        val = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        if val in lookup:
            team = lookup[val]
            if team in self.drawn_tracker:
                messagebox.showinfo("Draw Info", f"{team} is already in the table!")
            else:
                self.add_to_table(team)
                self.drawn_tracker.append(team)
                self.update_sidebars()
        else:
            messagebox.showwarning("Error", "Club not found. Please check spelling.")

    def add_to_table(self, team):
        row = [team.upper()]
        for p in range(1, 5):
            h, a = self.master_sched[team][p]['H'], self.master_sched[team][p]['A']
            row.append(f"H: {h} | A: {a}")
        self.tree.insert("", "end", values=row)
        self.tree.yview_moveto(1)

    def draw_all(self):
        rem = [c for c in ALL_CLUBS if c not in self.drawn_tracker]
        for team in rem:
            self.add_to_table(team)
            self.drawn_tracker.append(team)
        self.update_sidebars()

if __name__ == "__main__":
    root = tk.Tk()  
    app = UCLDrawApp(root)
    root.mainloop()