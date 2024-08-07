import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from PIL import Image, ImageDraw, ImageTk

def download_video():
    url = url_entry.get()
    video_quality = video_quality_var.get()
    audio_quality = audio_quality_var.get()
    output_dir = output_dir_entry.get()

    if not url:
        messagebox.showerror("Input Error", "Please enter a YouTube link.")
        return
    
    if not output_dir:
        messagebox.showerror("Input Error", "Please select an output directory.")
        return
    
    if video_quality and audio_quality:
        format_str = f"{video_quality}+{audio_quality}"
    elif video_quality:
        format_str = video_quality
    elif audio_quality:
        format_str = audio_quality
    else:
        format_str = "best"
    
    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s')
    }
    
    try:
        subprocess.run(['yt-dlp', '-f', format_str, '-o', ydl_opts['outtmpl'], url], check=True)
        messagebox.showinfo("Success", "Download completed successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Download Error", f"An error occurred: {e}")

def open_directory_picker(event):
    directory = filedialog.askdirectory()
    if directory:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, directory)

def create_rounded_button_image(width, height, radius, color):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width, height], radius, fill=color)
    return img

root = tk.Tk()
root.title("YouTube Video Downloader")
root.configure(bg="#f5f5f5")
root.geometry("800x500")

padx = 10
pady = 10
label_font = ('Helvetica', 12, 'bold')
entry_font = ('Helvetica', 12)
button_font = ('Helvetica', 12, 'bold')
button_bg_color = "#3e3892"
button_fg = "white"
button_width = 200
button_height = 50
button_radius = 25

rounded_button_image = create_rounded_button_image(button_width, button_height, button_radius, button_bg_color)
rounded_button_photo = ImageTk.PhotoImage(rounded_button_image)

header_frame = tk.Frame(root, bg="#3e3892", padx=20, pady=10)
header_frame.pack(fill='x')

header_label = tk.Label(header_frame, text="YouTube Downloader", font=('Helvetica', 20, 'bold'), fg="white", bg="#3e3892", anchor='w')
header_label.pack(side='left')

main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(expand=True)

tk.Label(main_frame, text="YouTube Link:", font=label_font, bg="#f5f5f5", anchor='w').grid(row=0, column=0, padx=padx, pady=pady, sticky='w')
url_entry = tk.Entry(main_frame, width=50, font=entry_font)
url_entry.grid(row=0, column=1, padx=padx, pady=pady, columnspan=2, sticky='ew')

tk.Label(main_frame, text="Video Quality:", font=label_font, bg="#f5f5f5", anchor='w').grid(row=1, column=0, padx=padx, pady=pady, sticky='w')
video_quality_var = tk.StringVar(root)
video_quality_var.set("")
video_quality_options = ["", "bestvideo", "2160p", "1440p", "1080p", "720p", "480p"]
video_quality_menu = tk.OptionMenu(main_frame, video_quality_var, *video_quality_options)
video_quality_menu.config(font=entry_font)
video_quality_menu.grid(row=1, column=1, padx=padx, pady=pady, sticky='ew')

tk.Label(main_frame, text="Audio Quality:", font=label_font, bg="#f5f5f5", anchor='w').grid(row=2, column=0, padx=padx, pady=pady, sticky='w')
audio_quality_var = tk.StringVar(root)
audio_quality_var.set("")
audio_quality_options = ["", "bestaudio", "256k", "128k", "64k"]
audio_quality_menu = tk.OptionMenu(main_frame, audio_quality_var, *audio_quality_options)
audio_quality_menu.config(font=entry_font)  
audio_quality_menu.grid(row=2, column=1, padx=padx, pady=pady, sticky='ew')

tk.Label(main_frame, text="Output Directory:", font=label_font, bg="#f5f5f5", anchor='w').grid(row=3, column=0, padx=padx, pady=pady, sticky='w')
output_dir_entry = tk.Entry(main_frame, width=50, font=entry_font)
output_dir_entry.grid(row=3, column=1, padx=padx, pady=pady, sticky='ew')

output_dir_entry.bind("<Button-1>", open_directory_picker)

download_button = tk.Button(main_frame, text="Download", command=download_video, font=button_font, image=rounded_button_photo, compound='center', relief='flat')
download_button.grid(row=4, column=1, padx=padx, pady=pady)

root.mainloop()
