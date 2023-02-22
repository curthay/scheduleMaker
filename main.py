import tkinter as tk

# Define the shift timings for each location
location1_shifts = [
    {"name": "0800-1700", "start_time": 800, "end_time": 1700},
    {"name": "1000-2000", "start_time": 1000, "end_time": 2000},
    {"name": "1700-0200", "start_time": 1700, "end_time": 200},
]
location2_shifts = [
    {"name": "0800-1900", "start_time": 800, "end_time": 1900},
]

# Define the maximum number of hours an employee can work in a week
MAX_HOURS_PER_WEEK = 40

# Define a function to create the schedule
def create_schedule():
    # Get the selected shift for each employee
    employee_shifts = []
    for i in range(len(employee_checkboxes)):
        employee_name = employee_checkboxes[i]["text"]
        selected_shift = None
        for shift in location1_shifts + location2_shifts:
            if shift_checkboxes[shift["name"]][i].get() == 1:
                selected_shift = shift
                break
        employee_shifts.append((employee_name, selected_shift))
    
    # Check if any employee is scheduled for two shifts in a row
    for i in range(len(employee_shifts) - 1):
        if employee_shifts[i][1] is not None and employee_shifts[i+1][1] is not None:
            if employee_shifts[i][1]["name"] == "1700-0200" and employee_shifts[i+1][1]["name"] == "0800-1700":
                employee_shifts[i+1] = (employee_shifts[i+1][0], None)
    
    # Assign shifts to each employee for the week
    schedule = []
    for shift in location1_shifts + location2_shifts:
        employees_available = [employee_shifts[i][0] for i in range(len(employee_shifts)) if employee_shifts[i][1] == shift]
        while len(employees_available) > 0:
            for employee in employees_available:
                if sum([1 for s in schedule if s[0] == employee]) < 5 and sum([s[1]["end_time"] - s[1]["start_time"] for s in schedule if s[0] == employee]) < MAX_HOURS_PER_WEEK:
                    schedule.append((employee, shift))
                    employees_available.remove(employee)
                    break
    
    # Display the schedule
    for shift in location1_shifts + location2_shifts:
        shift_name = shift["name"]
        employees_assigned = [s[0] for s in schedule if s[1] == shift]
        print(f"{shift_name}: {', '.join(employees_assigned)}")

# Create the GUI
root = tk.Tk()
root.title("Schedule Creator")

# Create the employee checkboxes
employee_checkboxes = []
for i in range(14):
    employee_name = f"Employee {i+1}"
    checkbox = tk.Checkbutton(root, text=employee_name)
    checkbox.grid(row=i+1, column=0)
    employee_checkboxes.append(checkbox)

# Create the shift checkboxes for each location
shift_checkboxes = {}
row = 1
for shift in location1_shifts:
  shift_name = shift["name"]
tk.Label(root, text=shift_name).grid(row=0, column=row)
for i in range(14):
  checkbox = tk.Checkbutton(root)
  checkbox.grid(row=i+1, column=row)
if shift_name == "1700-0200":
  checkbox["state"] = tk.DISABLED
  shift_checkboxes[shift_name] = shift_checkboxes.get(shift_name, []) + [checkbox]
  row += 1
for shift in location2_shifts:
  shift_name = shift["name"]
  tk.Label(root, text=shift_name).grid(row=0, column=row)
for i in range(14):
  checkbox = tk.Checkbutton(root)
  checkbox.grid(row=i+1, column=row)
  shift_checkboxes[shift_name] = shift_checkboxes.get(shift_name, []) + [checkbox]
  row += 1

# Create the Create Schedule Button
create_button = tk.Button(root, text="Create Schedule", command=create_schedule)
create_button.grid(row=15, column=1)

root.mainloop()
