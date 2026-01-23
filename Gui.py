# gui.py
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox

from City import City
from driver import Driver
from rider import Rider
from DispatchEngine import DispatchEngine
from RollBackManager import RollbackManager
from RideShareSystem import RideShareSystem
from Trip import Trip

# ---------------- Vice City palette ----------------
BG_DARK = "#0f172a"
CARD_BG = "#111827"
TEXT = "#e5e7eb"
ACCENT = "#93c5fd"
NEON_PINK = "#ff3ea5"
NEON_CYAN = "#00e5ff"
NEON_PURPLE = "#a78bfa"
NEON_YELLOW = "#ffd166"
GRID = "#1f2937"
WATER = "#0ea5e9"
SKYLINE = "#1d4ed8"

class RideShareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ride Sharing — Vice City Edition")
        self.root.geometry("1200x760")

        # ---------- Theme ----------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG_DARK)
        style.configure("Card.TFrame", background=CARD_BG, relief="groove", borderwidth=1)
        style.configure("TLabel", background=BG_DARK, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=BG_DARK, foreground=ACCENT, font=("Segoe UI Semibold", 14))
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.map("TButton", background=[("active", SKYLINE)])

        # ---------- Core system ----------
        self.city = City()
        # Base graph
        self.city.add_road("A", "B", 5)
        self.city.add_road("B", "C", 3)
        self.city.add_road("A", "D", 7)
        self.city.add_road("D", "C", 4)
        # Optional extra nodes for map flavor
        self.city.add_road("C", "E", 6)
        self.city.add_road("B", "E", 4)

        self.drivers = [
            Driver(1, "A", "Zone1"),
            Driver(2, "C", "Zone2"),
            Driver(3, "D", "Zone1"),
        ]

        self.dispatch = DispatchEngine(self.city)
        self.rollback = RollbackManager()
        self.system = RideShareSystem(self.dispatch, self.rollback)

        # ---------- Layout ----------
        container = ttk.Frame(root, padding=14, style="TFrame")
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Ride-Sharing Dispatch & Trip Management — Vice City Map", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 10))

        panes = ttk.Frame(container, style="TFrame")
        panes.pack(fill="both", expand=True)

        left = ttk.Frame(panes, padding=12, style="Card.TFrame")
        mid = ttk.Frame(panes, padding=12, style="Card.TFrame")
        right = ttk.Frame(panes, padding=12, style="Card.TFrame")

        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        mid.grid(row=0, column=1, sticky="nsew", padx=(0, 12))
        right.grid(row=0, column=2, sticky="nsew")

        panes.columnconfigure(0, weight=1)
        panes.columnconfigure(1, weight=2)
        panes.columnconfigure(2, weight=2)
        panes.rowconfigure(0, weight=1)

        # ---------- Left: Controls ----------
        ttk.Label(left, text="Rider request", style="Card.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(left, text="Pickup:", style="Card.TLabel").grid(row=1, column=0, sticky="e", pady=2)
        self.pickup_entry = ttk.Entry(left, width=18)
        self.pickup_entry.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(left, text="Dropoff:", style="Card.TLabel").grid(row=2, column=0, sticky="e", pady=2)
        self.dropoff_entry = ttk.Entry(left, width=18)
        self.dropoff_entry.grid(row=2, column=1, sticky="w", pady=2)

        ttk.Label(left, text="Preferred zone:", style="Card.TLabel").grid(row=3, column=0, sticky="e", pady=2)
        self.zone_var = tk.StringVar(value="Any")
        self.zone_menu = ttk.Combobox(left, textvariable=self.zone_var, values=["Any", "Zone1", "Zone2", "Zone3"], state="readonly", width=16)
        self.zone_menu.grid(row=3, column=1, sticky="w", pady=2)

        ttk.Button(left, text="Request Trip", command=self.request_trip).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 2))
        ttk.Button(left, text="Complete Selected", command=self.complete_selected).grid(row=5, column=0, columnspan=2, sticky="ew", pady=2)
        ttk.Button(left, text="Cancel Selected", command=self.cancel_selected).grid(row=6, column=0, columnspan=2, sticky="ew", pady=2)

        ttk.Separator(left).grid(row=7, column=0, columnspan=2, sticky="ew", pady=8)

        ttk.Label(left, text="Rollback (k ops):", style="Card.TLabel").grid(row=8, column=0, sticky="e", pady=2)
        self.k_entry = ttk.Entry(left, width=6)
        self.k_entry.insert(0, "1")
        self.k_entry.grid(row=8, column=1, sticky="w", pady=2)

        ttk.Button(left, text="Rollback", command=self.rollback_k).grid(row=9, column=0, columnspan=2, sticky="ew", pady=(6, 2))

        ttk.Separator(left).grid(row=10, column=0, columnspan=2, sticky="ew", pady=8)

        ttk.Label(left, text="Add road (u, v, w):", style="Card.TLabel").grid(row=11, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.u_entry = ttk.Entry(left, width=6); self.u_entry.grid(row=12, column=0, sticky="w", pady=2)
        self.v_entry = ttk.Entry(left, width=6); self.v_entry.grid(row=12, column=1, sticky="w", pady=2)
        self.w_entry = ttk.Entry(left, width=6); self.w_entry.grid(row=13, column=0, sticky="w", pady=2)
        ttk.Button(left, text="Add Road", command=self.add_road).grid(row=13, column=1, sticky="ew", pady=2)

        for i in range(14):
            left.rowconfigure(i, weight=0)
        left.columnconfigure(0, weight=1)
        left.columnconfigure(1, weight=1)

        # ---------- Middle: Trip history ----------
        ttk.Label(mid, text="Trip history", style="Card.TLabel").pack(anchor="w", pady=(0, 8))
        columns = ("ID", "Driver", "Pickup", "Dropoff", "State", "Distance")
        self.history = ttk.Treeview(mid, columns=columns, show="headings", height=22)
        for col in columns:
            self.history.heading(col, text=col)
        self.history.column("ID", width=60, anchor="center")
        self.history.column("Driver", width=80, anchor="center")
        self.history.column("Pickup", width=100, anchor="center")
        self.history.column("Dropoff", width=100, anchor="center")
        self.history.column("State", width=110, anchor="center")
        self.history.column("Distance", width=90, anchor="center")
        self.history.pack(fill="both", expand=True)

        # ---------- Right: Map + Drivers + Analytics ----------
        top_right = ttk.Frame(right, style="Card.TFrame")
        top_right.pack(fill="x", pady=(0, 10))
        ttk.Label(top_right, text="Drivers", style="Card.TLabel").pack(anchor="w", pady=(0, 6))

        self.drivers_list = ttk.Treeview(top_right, columns=("ID", "Loc", "Zone", "Avail"), show="headings", height=6)
        for c in ("ID", "Loc", "Zone", "Avail"):
            self.drivers_list.heading(c, text=c)
        self.drivers_list.column("ID", width=50, anchor="center")
        self.drivers_list.column("Loc", width=70, anchor="center")
        self.drivers_list.column("Zone", width=70, anchor="center")
        self.drivers_list.column("Avail", width=70, anchor="center")
        self.drivers_list.pack(fill="x")

        map_frame = ttk.Frame(right, style="Card.TFrame")
        map_frame.pack(fill="both", expand=True, pady=(0, 10))
        ttk.Label(map_frame, text="Vice City Mini‑Map", style="Card.TLabel").pack(anchor="w", pady=(0, 6))

        self.map_canvas = tk.Canvas(map_frame, width=520, height=420, bg=BG_DARK, highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True)

        analytics_frame = ttk.Frame(right, style="Card.TFrame")
        analytics_frame.pack(fill="x")
        ttk.Label(analytics_frame, text="Analytics", style="Card.TLabel").pack(anchor="w", pady=(8, 6))
        self.analytics_text = tk.Text(analytics_frame, height=10, bg=BG_DARK, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.analytics_text.pack(fill="x")
        ttk.Button(analytics_frame, text="Refresh Analytics", command=self.refresh_analytics).pack(fill="x", pady=(8, 0))

        # ---------- Map model ----------
        # Zones (rects) and node positions (Vice City vibe)
        self.zones = {
            "Zone1": (20, 40, 240, 220, NEON_PURPLE),
            "Zone2": (260, 40, 500, 220, NEON_CYAN),
            "Zone3": (20, 240, 500, 400, NEON_PINK),
        }
        self.node_positions = {
            "A": (60, 180),
            "B": (180, 80),
            "C": (420, 180),
            "D": (220, 320),
            "E": (340, 100),
        }
        self.driver_icons = {}  # driver_id -> canvas item id

        self.draw_map_base()
        self.draw_graph()
        self.refresh_drivers()
        self.refresh_analytics()

    # ---------------- Map drawing ----------------
    def draw_map_base(self):
        c = self.map_canvas
        w = int(c["width"]); h = int(c["height"])
        c.delete("all")

        # Skyline band
        c.create_rectangle(0, 0, w, 30, fill=SKYLINE, outline="")
        # Water strip
        c.create_rectangle(0, h-40, w, h, fill=WATER, outline="")

        # Grid
        for x in range(0, w, 40):
            c.create_line(x, 30, x, h-40, fill=GRID)
        for y in range(30, h-40, 40):
            c.create_line(0, y, w, y, fill=GRID)

        # Zones
        for name, (x1, y1, x2, y2, color) in self.zones.items():
            c.create_rectangle(x1, y1, x2, y2, outline=color, width=2)
            c.create_text((x1+x2)//2, y1+14, text=name, fill=color, font=("Segoe UI", 10, "bold"))

    def draw_graph(self):
        c = self.map_canvas
        # Edges
        drawn = set()
        for src in self.city.graph:
            for dest, dist in self.city.graph[src]:
                key = tuple(sorted((src, dest)))
                if key in drawn: 
                    continue
                drawn.add(key)
                x1, y1 = self.node_positions.get(src, (0, 0))
                x2, y2 = self.node_positions.get(dest, (0, 0))
                c.create_line(x1, y1, x2, y2, fill=TEXT, width=2)
                c.create_text((x1+x2)//2, (y1+y2)//2, text=str(dist), fill=NEON_YELLOW, font=("Segoe UI", 9))

        # Nodes
        for node, (x, y) in self.node_positions.items():
            c.create_oval(x-12, y-12, x+12, y+12, fill=ACCENT, outline="")
            c.create_text(x, y, text=node, fill=BG_DARK, font=("Segoe UI", 10, "bold"))

        # Driver icons
        for d in self.drivers:
            self._draw_driver_icon(d)

    def _draw_driver_icon(self, driver):
        c = self.map_canvas
        x, y = self.node_positions.get(driver.location, (None, None))
        if x is None:
            return
        color = NEON_CYAN if driver.available else NEON_PINK
        # Triangle marker
        icon = c.create_polygon(x, y-16, x-10, y+10, x+10, y+10, fill=color, outline="")
        label = c.create_text(x, y+20, text=f"D{driver.driver_id}", fill=color, font=("Segoe UI", 9, "bold"))
        self.driver_icons[driver.driver_id] = (icon, label)

    def _move_driver_icon(self, driver):
        # Repaint icon to reflect availability color
        ids = self.driver_icons.get(driver.driver_id)
        if not ids:
            self._draw_driver_icon(driver)
            return
        icon, label = ids
        color = NEON_CYAN if driver.available else NEON_PINK
        self.map_canvas.itemconfig(icon, fill=color)
        self.map_canvas.itemconfig(label, fill=color)

    def _highlight_path(self, path, color):
        if not path or len(path) < 2:
            return
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            x1, y1 = self.node_positions.get(a, (0, 0))
            x2, y2 = self.node_positions.get(b, (0, 0))
            self.map_canvas.create_line(x1, y1, x2, y2, fill=color, width=4)

    # ---------------- Dijkstra (route) for GUI ----------------
    def _shortest_route(self, start, end):
        # GUI-local Dijkstra to get the actual path (City.shortest_path returns distance only)
        import heapq
        graph = self.city.graph
        if start not in graph or end not in graph:
            return [], float("inf")
        dist = {n: float("inf") for n in graph}
        prev = {n: None for n in graph}
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                break
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        if dist[end] == float("inf"):
            return [], float("inf")
        # Reconstruct path
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path, dist[end]

    # ---------------- Actions ----------------
    def request_trip(self):
        pickup = self.pickup_entry.get().strip()
        dropoff = self.dropoff_entry.get().strip()
        zone_pref = self.zone_var.get()

        if not pickup or not dropoff:
            messagebox.showerror("Error", "Pickup and dropoff are required.")
            return
        if pickup not in self.city.graph or dropoff not in self.city.graph:
            messagebox.showerror("Error", "Pickup/dropoff must exist in the city graph.")
            return

        rider = Rider(100 + len(self.system.trips) + 1, pickup, dropoff)

        # Zone-aware preference
        candidate = self.drivers
        if zone_pref != "Any":
            in_zone = [d for d in self.drivers if d.zone == zone_pref and d.available]
            if in_zone:
                candidate = in_zone

        driver, distance = self.dispatch.assign_driver(candidate, rider)
        if not driver:
            messagebox.showwarning("No Driver", "No available driver found for this request.")
            return

        trip_id = len(self.system.trips) + len(self.system.completed_trips) + len(self.system.cancelled_trips) + 1
        trip = self.system.request_trip(trip_id, rider, self.drivers)
        if not trip:
            messagebox.showerror("Error", "Trip could not be created.")
            return

        # Update UI
        self.append_history_row(trip)
        self.refresh_drivers()
        self.refresh_analytics()

        # Map: highlight driver→pickup and pickup→dropoff
        self.draw_map_base()
        self.draw_graph()
        path1, _ = self._shortest_route(driver.location, pickup)
        path2, _ = self._shortest_route(pickup, dropoff)
        self._highlight_path(path1, NEON_YELLOW)
        self._highlight_path(path2, NEON_PINK)
        self._move_driver_icon(driver)

        messagebox.showinfo("Assigned", f"Trip {trip.trip_id} → Driver {trip.driver.driver_id} (distance {trip.distance}).")

    def cancel_selected(self):
        trip = self._get_selected_trip()
        if not trip:
            messagebox.showwarning("Select Trip", "Select a trip in the history table.")
            return
        if trip.state in ("COMPLETED", "CANCELLED"):
            messagebox.showwarning("Invalid", "Trip already finalized.")
            return

        self.system.cancel_trip(trip)
        self._update_history_row(trip)
        self.refresh_drivers()
        self.refresh_analytics()

        # Map refresh
        self.draw_map_base()
        self.draw_graph()
        self._move_driver_icon(trip.driver)

    def complete_selected(self):
        trip = self._get_selected_trip()
        if not trip:
            messagebox.showwarning("Select Trip", "Select a trip in the history table.")
            return
        if trip.state in ("COMPLETED", "CANCELLED"):
            messagebox.showwarning("Invalid", "Trip already finalized.")
            return

        self.system.complete_trip(trip)
        self._update_history_row(trip)
        self.refresh_drivers()
        self.refresh_analytics()

        # Map refresh
        self.draw_map_base()
        self.draw_graph()
        self._move_driver_icon(trip.driver)

    def rollback_k(self):
        k_text = self.k_entry.get().strip()
        try:
            k = int(k_text)
            if k <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a positive integer for k.")
            return

        rolled = 0
        while rolled < k:
            snapshot = self.rollback.rollback()
            if not snapshot:
                break
            trip, driver_state = snapshot
            trip.driver.available = driver_state
            self._update_history_row(trip)
            rolled += 1

        self.refresh_drivers()
        self.refresh_analytics()

        # Map refresh
        self.draw_map_base()
        self.draw_graph()
        for d in self.drivers:
            self._move_driver_icon(d)

        messagebox.showinfo("Rollback", f"Rolled back {rolled} operation(s).")

    def add_road(self):
        u = self.u_entry.get().strip()
        v = self.v_entry.get().strip()
        w_text = self.w_entry.get().strip()
        if not u or not v or not w_text:
            messagebox.showerror("Error", "Enter u, v, and w.")
            return
        try:
            w = float(w_text)
        except ValueError:
            messagebox.showerror("Error", "Weight must be a number.")
            return

        self.city.add_road(u, v, w)
        # If new nodes, add rough positions (you can tune these)
        if u not in self.node_positions:
            self.node_positions[u] = (60 + 40*len(self.node_positions), 320)
        if v not in self.node_positions:
            self.node_positions[v] = (60 + 40*(len(self.node_positions)+1), 320)

        self.draw_map_base()
        self.draw_graph()
        messagebox.showinfo("Road Added", f"Added road {u} ↔ {v} (w={w}).")

    # ---------------- Helpers ----------------
    def append_history_row(self, trip: Trip):
        self.history.insert(
            "",
            "end",
            iid=str(trip.trip_id),
            values=(trip.trip_id, trip.driver.driver_id, trip.rider.pickup, trip.rider.dropoff, trip.state, f"{trip.distance:.2f}")
        )

    def _update_history_row(self, trip: Trip):
        if str(trip.trip_id) in self.history.get_children():
            self.history.item(str(trip.trip_id), values=(
                trip.trip_id, trip.driver.driver_id, trip.rider.pickup, trip.rider.dropoff, trip.state,
                f"{trip.distance:.2f}"
            ))
        else:
            self.append_history_row(trip)

    def _get_selected_trip(self):
        sel = self.history.selection()
        if not sel:
            return None
        trip_id = int(sel[0])
        for t in self.system.trips + self.system.completed_trips + self.system.cancelled_trips:
            if t.trip_id == trip_id:
                return t
        return None

    def refresh_drivers(self):
        for row in self.drivers_list.get_children():
            self.drivers_list.delete(row)
        for d in self.drivers:
            self.drivers_list.insert("", "end", values=(d.driver_id, d.location, d.zone, "Yes" if d.available else "No"))

    def refresh_analytics(self):
        avg_distance = self._avg_distance()
        utilization = self._driver_utilization()
        counts = self._counts()

        self.analytics_text.delete("1.0", "end")
        self.analytics_text.insert("end", f"Total trips: {counts['total']}\n")
        self.analytics_text.insert("end", f"Completed: {counts['completed']} | Cancelled: {counts['cancelled']} | Active: {counts['active']}\n")
        self.analytics_text.insert("end", f"Average trip distance: {avg_distance:.2f}\n")
        self.analytics_text.insert("end", "Driver utilization (assigned at least once):\n")
        for did, used in utilization.items():
            self.analytics_text.insert("end", f"  - Driver {did}: {'Yes' if used else 'No'}\n")

    # ---------- Analytics ----------
    def _avg_distance(self):
        distances = [t.distance for t in (self.system.completed_trips + self.system.cancelled_trips + self.system.trips)]
        return sum(distances) / len(distances) if distances else 0.0

    def _driver_utilization(self):
        used = {d.driver_id: False for d in self.drivers}
        for t in self.system.trips + self.system.completed_trips + self.system.cancelled_trips:
            used[t.driver.driver_id] = True
        return used

    def _counts(self):
        return {
            "total": len(self.system.trips) + len(self.system.completed_trips) + len(self.system.cancelled_trips),
            "completed": len(self.system.completed_trips),
            "cancelled": len(self.system.cancelled_trips),
            "active": len(self.system.trips),
        }


if __name__ == "__main__":
    root = tk.Tk()
    app = RideShareGUI(root)
    root.mainloop()
