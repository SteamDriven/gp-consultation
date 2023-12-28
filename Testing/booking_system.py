import tkinter as tk
from datetime import datetime, timedelta

import tkcalendar


class TimeSelectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Selector")

        # Create and place widgets
        self.label = tk.Label(master, text="Select a day and available times:")
        self.label.pack(pady=10)

        self.today_button = tk.Button(master, text="Today", command=lambda: self.populate_buttons(datetime.now()))
        self.today_button.pack(side=tk.LEFT, padx=5)

        self.tomorrow_button = tk.Button(master, text="Tomorrow",
                                         command=lambda: self.populate_buttons(datetime.now() + timedelta(days=1)))
        self.tomorrow_button.pack(side=tk.LEFT, padx=5)

        self.select_date_button = tk.Button(master, text="Select Date", command=self.select_date)
        self.select_date_button.pack(side=tk.LEFT, padx=5)

        self.available_times_frame = tk.Frame(master)
        self.available_times_frame.pack(pady=10)

        self.select_button = tk.Button(master, text="Select", command=self.get_selected_times)
        self.select_button.pack(pady=10)

    def populate_buttons(self, selected_date):
        # Clear previous buttons
        for widget in self.available_times_frame.winfo_children():
            widget.destroy()

        # Add available times as buttons for the selected date
        available_times = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
        for time in available_times:
            time_button = tk.Button(self.available_times_frame, text=time,
                                    command=lambda t=time: self.handle_time_selection(selected_date, t))
            time_button.pack(side=tk.LEFT, padx=5)

    def select_date(self):
        # Open a separate window to select a specific date
        date_selector_window = tk.Toplevel(self.master)
        date_selector_window.title("Select Date")

        # Calendar widget for date selection
        cal = tkcalendar.Calendar(date_selector_window, selectmode="day", year=datetime.now().year, month=datetime.now().month,
                          day=datetime.now().day)
        cal.pack(padx=10, pady=10)

        # Button to confirm the selected date
        confirm_button = tk.Button(date_selector_window, text="Select",
                                   command=lambda: self.handle_selected_date(cal.get_date()))
        confirm_button.pack(pady=10)

    def handle_selected_date(self, selected_date):
        # Close the date selector window and update the available times based on the selected date
        self.populate_buttons(datetime(selected_date[0], selected_date[1], selected_date[2]))
        self.master.focus_set()

    def handle_time_selection(self, selected_date, selected_time):
        # Handle the selection of a specific time
        print(f"Selected time: {selected_date.strftime('%Y-%m-%d')} {selected_time}")

    def get_selected_times(self):
        # Implement your logic for handling selected times here
        print("Implement your logic here")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeSelectorApp(root)
    root.mainloop()
