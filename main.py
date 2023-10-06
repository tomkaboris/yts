import tkinter as tk
from tkinter import scrolledtext
import requests
import webbrowser
from bs4 import BeautifulSoup

def on_enter(event):
    text.tag_configure("mytag", foreground="blue", underline=True)
    text.config(cursor="hand2")

def on_leave(event):
    text.tag_configure("mytag", foreground="black", underline=False)
    text.config(cursor="")

def open_link(event):
    index = text.index(tk.CURRENT)
    torrentUrl = text.tag_names(index)
    webbrowser.open(str(torrentUrl[0]))

def clear_search():
    # Clear the Text widget
    text.delete(1.0, tk.END)

def get_movie_info():
    movie_title = entry.get()

    if movie_title:
        url = f"https://yts.mx/api/v2/list_movies.json?query_term={movie_title.replace(' ', '-').lower()}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Access specific information from the JSON response
                if 'data' in data and 'movies' in data['data']:
                    movies = data['data']['movies']

                    for movie in movies:
                        title = movie['title']
                        rating = movie['rating']
                        year = movie['year']
                        torrents = movie['torrents']
                        slug = movie['slug']

                        suburl = f"https://yts.mx/movies/{slug}"
                        reqs = requests.get(suburl)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        subtitle = ''
                        for link in soup.find_all('a'):
                            if "yifysubtitles.ch" in link.get('href'):
                                subtitle = link.get('href')

                        # Display the movie title and description
                        text.insert(tk.END, f"Title: {title}\n")
                        text.insert(tk.END, f"Year: {year}\n")
                        text.insert(tk.END, f"Rating IMDb: {str(rating)}\n")

                        if subtitle != '':
                            text.insert(tk.END, f"Subtitles link\n", subtitle)
                            text.tag_configure(subtitle, foreground="blue")
                            text.tag_bind(subtitle, "<Enter>", on_enter)
                            text.tag_bind(subtitle, "<Leave>", on_leave)
                            text.tag_bind(subtitle, "<Button-1>", open_link)
                        else:
                            text.insert(tk.END, f"Subtitle: None\n")
                        text.insert(tk.END, f"Torrents:\n")

                        for torrent in torrents:
                            quality = torrent['quality']
                            size = torrent['size']
                            torrentUrl = torrent['url']

                            text.insert(tk.END, f"  Size[{quality}]: {size}", torrentUrl)
                            # Configure the hyperlink tag
                            text.tag_configure(torrentUrl, foreground="blue")

                            # Bind the <Enter> and <Leave> events to change the tag appearance and cursor
                            text.tag_bind(torrentUrl, "<Enter>", on_enter)
                            text.tag_bind(torrentUrl, "<Leave>", on_leave)

                            # Bind the function to the hyperlink tag
                            text.tag_bind(torrentUrl, "<Button-1>", open_link)

                            text.insert(tk.END, "\n")


                        text.insert(tk.END, "====================================================\n")
                else:
                    text.insert(tk.END, f"There is no movie '{movie_title}', please try again!\n")
            else:
                print(f"Error: Status Code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error decoding JSON: {e}")


# Create root window
window = tk.Tk()
# Root window title and dimension
window.title("Download movie from www.yts.mx")
# Set geometry (width x height)
window.geometry('800x600')
# To make the GUI dimensions fixed
window.resizable(False, False)

# Adding Entry Label
entry_label = tk.Label(window, text="Enter Movie Title:")
entry_label.pack(pady=2)

# Adding Entry Field
entry = tk.Entry(window, width=100)
entry.pack(pady=2)

# Create a frame to contain the buttons
button_frame = tk.Frame(window)
button_frame.pack()

get_info_button = tk.Button(button_frame, text="Get Movie Info", command=get_movie_info)
get_info_button.pack(side=tk.LEFT, padx=2)

clear_button = tk.Button(button_frame, text="Clear", command=clear_search)
clear_button.pack(side=tk.LEFT, padx=2)

text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=100)
text.pack(pady=2)

# Execute Tkinter
window.mainloop()
