import webbrowser
import sys

q = sys.argv[1]

url = f"https://www.google.com/search?q={q}"
webbrowser.open_new_tab(url)
