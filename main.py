from pytube import *
from tkinter import *
from tkinter.ttk import Progressbar
import os
from tkinter import messagebox as msg


def search():
    desc_area.insert("1.0", END)
    url = vedio_url.get()
    try:
        if url == "":
            error_msg.set("Please Enter URL of the Vedio.")
        else:
            yt = YouTube(url)
            title.set(yt.title)
            desc_area.insert(END, str(yt.description))
            if v.get() == "Vedio":
                download_size = (YouTube(url).streams.first().filesize)/1024000
                cont_size.set(f"Download Size: {round(download_size,2)} MB")
            if v.get() == "Audio":
                download_size = (YouTube(url).streams.filter(
                    only_audio=True).first().filesize)/1024000
                cont_size.set(f"Download Size: {round(download_size,2)} MB")

    except:
        error_msg.set("Please Enter Valid URL of the Vedio.")


def clear():
    desc_area.delete("1.0", END)
    vedio_url.set("")
    title.set("")
    cont_size.set("Download Size: 0 MB")
    error_msg.set("")
    v.set("Vedio")


def progress_(streams, chunk, bytes_remaining):
    
    if v.get() == "Vedio":
        download_size = (
            YouTube(vedio_url.get()).streams.first().filesize)/1024000
        percentage = (
            float(abs(bytes_remaining - download_size)/download_size) * 100)
    if v.get() == "Audio":
        download_size = (YouTube(vedio_url.get()).streams.filter(
            only_audio=True).first().filesize)/1024000
        percentage = (
            float(abs(bytes_remaining - download_size)/download_size) * 100)
    progress["value"] = percentage
    progress.update()
    lbl_download.config = Label(f5, text=f"Downloading {round(percentage,2)}%")


def download():
    search()
    url = vedio_url.get()
    try:
        if url == "":
            error_msg.set("Please Enter URL of Vedio.")
        else:
            if v.get() == "Vedio":
                yt = YouTube(url, on_progress_callback=progress_)
                yt.streams.first().download("Vedio/")
            if v.get() == "Audio":
                yt = YouTube(url, on_progress_callback=progress_)
                yt.streams.filter(only_audio=True).first().download("Audio/")
    except:
        error_msg.set("Please Enter Valid URL of the Vedio.")


def makeDir():
    if os.path.isdir("Vedio") and os.path.isdir("Audio"):
        pass
    else:
        os.mkdir("Vedio")
        os.mkdir("Audio")


root = Tk()
makeDir()
root.geometry("550x390+550+180")
root.resizable(False, False)
root.title("Youtube Video Downloader | Developed by Randeep")

vedio_url = StringVar()
title = StringVar()

Label(text="Youtube Video Downloader | Developed by Randeep", font=("times new roman",
                                                                    18, "bold"), foreground="white", background="black", pady=5).pack(fill="x")

# =============Url Taking Frame===========
f1 = Frame(root, bg="black", pady=5)
f1.place(x=1, y=42)

lbl = Label(f1, text=" Video URL:", font=("times new roman", 14, "bold"),
            fg="white", bg="black", padx=20).grid(row=0, column=0)
url_entry = Entry(f1, width=45, bd=5, relief="sunken",
                  textvariable=vedio_url).grid(row=0, column=1, padx=5)

Button(f1, text="Search", font=("times new roman", 11, "bold"), padx=15, bg="green",
       fg="white", bd=3, relief="groove", command=search).grid(row=0, column=2, padx=20)
# =================Vedio Thumbnail Frame===========
f2 = Frame(root, bg="black")
f2.place(x=1, y=86, height=135, width=150)
lbl_thumbnail = Label(f2, text="Video Thumbnail", bd=4,
                      relief="groove", height=8, width=19).pack(pady=2)
# =================Vedio Title Frame=============
f3 = Frame(root, bg="black", bd=5, relief="sunken")
f3.place(x=153, y=86, width=395, height=170)

lbl = Label(f3, text="Video Title:", font=("times new roman", 12,
                                           "bold"), bg="black", fg="white").grid(row=0, column=0)
title_entry = Entry(f3, font="lucida 8 bold", width=48, bd=2,
                    relief="sunken", textvariable=title).grid(row=0, column=1, padx=2)

# ==========Description Frame=============
f4 = LabelFrame(f3, text="Decription", font=("times new roman",
                                             12, "bold"), fg="gold", bg="black", bd=3, relief="groove")
f4.place(x=1, y=25)

desc_area = Text(f4, font=("times new roman", 10),
                 width=62, height=6.9)
desc_area.pack()
desc_area.config(bg="light yellow")
# =============Downloading buttun Frame=========
f5 = Frame(root)
f5.place(x=153, y=260, width=390, height=39)
cont_size = StringVar()
lbl_size = Label(f5, text="Downloading Size: 0 MB", textvariable=cont_size).grid(
    row=0, column=0, sticky="w")

lbl_download = Label(f5, text="Downloading 0%")
lbl_download.grid(row=1, column=0, sticky="w")


f6 = Frame(f5)
f6.place(x=230, y=5)
Button(f6, text="Download", font=("times new roman", 11, "bold"),
       fg="white", bg="green", command=download).grid(row=0, column=0, padx=3)
Button(f6, text="Clear", font=("times new roman", 11, "bold"),
       padx=12, command=clear).grid(row=0, column=1)

# ==========Radio Button Frame==========

f7 = Frame(root, bd=4, relief="groove")
f7.place(x=1, y=222, width=149, height=82)

Label(f7, text="Download Format", font="lucida 10 bold", fg="red", pady=3).pack()

v = StringVar()
v.set("Vedio")

vedio_radio = Radiobutton(f7, text="Video", font="lucida 11",
                          fg="black", value="Vedio", variable=v).pack()
audio_radio = Radiobutton(f7, text="Audio", font="lucida 11",
                          fg="black", value="Audio", variable=v).pack()

# ==============ProgressBar Frame==========
download_status =0
f8 = Frame(root, bg="black")
f8.place(x=2, y=305, width=546, height=30)

progress_lbl = Label(f8, text=" Downloading Progress:",
                     font="helvatica 10 bold", fg="white", bg="black").grid(row=0, column=0)
progress = Progressbar(f8, orient=HORIZONTAL,
                       length=360, mode='determinate').grid(row=0, column=1, padx=15, pady=4)
# =============Footer Frame=========
f9 = Frame(root, bg="black")
f9.place(x=2, y=338, width=546, height=50)
Label(f9, text="©Copyright by Randeep\nAll Rights Reserved",
      font="helvatica 11", fg="white", bg="black").pack()
error_msg = StringVar()
error_lbl = Label(f9, text="", font="lucida 12 bold",
                  fg="red", bg="black", textvariable=error_msg).pack()


root.mainloop()
