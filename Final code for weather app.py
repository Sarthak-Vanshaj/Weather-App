import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def get_weather(city):
    api_key = '65500561c70960db7e687ad3bf3ea4d4'
    base_url = 'http://api.weatherstack.com/current'
    
    params = {
        'access_key': api_key,
        'query': city,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raising an exception for HTTP errors

        data = response.json()

        if 'current' in data:
            display_weather(data['current'], city)
        else:
            messagebox.showerror('Error', f'Unable to fetch weather data for {city}')
    except requests.exceptions.RequestException as e:
        handle_api_error(e)

def display_weather(data, city):
    weather_description = data['weather_descriptions'][0]
    temperature = data['temperature']
    humidity = data['humidity']
    wind_speed = data['wind_speed']

    result = (
        f"Weather in {city}: {weather_description}\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} km/h\n"
    )
    result_label.config(text=result)

def handle_api_error(error):
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 404:
            messagebox.showerror('Error', 'City not found. Please check the spelling and try again.')
        else:
            messagebox.showerror('Error', f'API request failed: {error}')
    else:
        messagebox.showerror('Error', f'API request failed: {error}')
    
      # Getting the current window size
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Resizing the background image to fit the window using LANCZOS resampling
    background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.image = background_photo

# Creating the main window
root = tk.Tk()
root.title('Weather App')
root.attributes('-alpha', 1)  # Setting transparency level for the main window

# Configuring window size and background color
root.geometry("1920x1080")

# Loading default background image
default_background_path = "Images\default_background.png"
default_background = Image.open(default_background_path)
default_background = default_background.resize((1920, 1080), Image.LANCZOS)
default_background_photo = ImageTk.PhotoImage(default_background)

# Background label for displaying Images
background_label = tk.Label(root, image=default_background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creating a frame for the UI elements
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
frame.configure(background=root.cget('bg'))  # Set frame background to match the root window background
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Creating and setting up UI elements
title_label = tk.Label(frame, text='Weather App', font=('Helvetica', 24, 'bold'), bg='#F0F0F0', fg='black')
title_label.pack(pady=10)

city_label = tk.Label(frame, text='Enter City:', font=('Helvetica', 14), bg='#F0F0F0', fg='black')
city_label.pack(pady=5)

city_entry = tk.Entry(frame, font=('Helvetica', 14))
city_entry.pack(pady=10, ipadx=10, ipady=5)

search_button = tk.Button(frame, text='Get Weather', command=lambda: get_weather(city_entry.get()), font=('Helvetica', 14, 'bold'), bg='#2ecc71', fg='black')
search_button.pack(pady=10)

result_label = tk.Label(frame, text='', font=('Helvetica', 18), bg='#F0F0F0', fg='black')
result_label.pack(pady=20)

# Binding the function to the window resize event
root.bind("<Configure>", lambda event: default_background("default"))

# Running the applicationas
root.mainloop()
