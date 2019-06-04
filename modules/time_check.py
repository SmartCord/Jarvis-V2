from datetime import datetime

v = datetime.now().strftime("%-I:%M %p")

print(f"It is currently {v}")
