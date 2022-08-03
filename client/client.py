from tkinter.filedialog import askopenfilename, askdirectory
import tkinter as tk
import pickle
import socket
import os
from PIL import ImageTk, Image

HOST = socket.gethostname()
PORT = 640

bColor = '#105F74'
fColor = '#FFFFFF'
tColor = '#CC2944'
hColor = '#848480'


def add_file():
    # global pathDownload
    type_files = 'pdf'
    file_path = askopenfilename(filetypes=[('all files', '.*')], title="Select files", multiple=True)
    if not file_path:
        return
    arrPath = file_path[0].split(fr'/')
    # pathDownload = fr'{arrPath[0]}/{arrPath[1]}/{arrPath[2]}/Downloads'
    for file in file_path:
        extension = file.split('.')
        if type_files == extension[1]:
            with open(file, 'rb') as binaryPdf:
                binPdf = binaryPdf.read()
            list_files.append(file)
            binary_files.append([os.path.basename(file), binPdf])
    render_list_item()


def delete_file(index):
    list_files.pop(index)
    binary_files.pop(index)
    render_list_item()


def render_list_item():
    global lab, btn_add
    for widgets in frm_names_item.winfo_children():
        widgets.destroy()
    for widgets in frm_buttons.winfo_children():
        widgets.destroy()
    if len(list_files) > 0:
        btn_save = tk.Button(frm_buttons, text="Send", width=4, command=save_file, bg=bColor, fg=fColor,
                             font=('Helvetica 12 bold'))
        btn_save.grid(row=1, column=0, sticky=tk.EW, padx=5)
    btn_add = tk.Button(frm_buttons, text="+", command=add_file, width=4, bg=bColor, fg=fColor,
                        font=('Helvetica 12 bold'))
    btn_add.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=10)
    for index, item in enumerate(list_files):
        extension = item.split('/')
        btn_del = tk.Button(frm_names_item, width=25, text=f"X- {extension[-1]}", fg=tColor, font=('Helvetica 12'),
                            command=lambda key=index: delete_file(key))
        btn_del.grid(row=index, column=10, padx=5, pady=5)


def save_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.connect((HOST, PORT))
        binPdf = pickle.dumps(binary_files)
        serverSocket.sendall(binPdf)
        size = serverSocket.recv(1024)
        recSize = pickle.loads(size)
        data = b""
        while True:
            binImage = serverSocket.recv(recSize)
            if len(binImage) <= recSize:
                data += binImage
                break
            data += binImage
    print(len(data))
    files_obj = pickle.loads(data)
    viewResponse(files_obj)


def viewResponse(imagePNG):
    for widgets in frm_names_item.winfo_children():
        widgets.destroy()
    for widgets in frm_buttons.winfo_children():
        widgets.destroy()
    lab.config(text='To download the images, click')
    btn_download = tk.Button(frm_names_item, text=f"Download", bg=bColor, fg=fColor,
                             command=lambda obj=imagePNG: save_image(obj), font=('Helvetica 12 bold'))
    btn_download.pack()


def save_image(images):
    pathDownload = askdirectory()
    for widgets in frm_names_item.winfo_children():
        widgets.destroy()
    labRes = tk.Label(frm_names_item, text='The download is in progress, please wait ....', fg=bColor, font=('Helvetica 12 bold'))
    labRes.grid()
    for imagePNG in images:
        path = fr'{pathDownload}/{imagePNG[0]}'
        with open(path, 'wb') as save:
            save.write(imagePNG[1])
    for widgets in frm_names_item.winfo_children():
        widgets.destroy()
    labRes.config(text='Finished ....')



if __name__ == '__main__':
    list_files = []
    binary_files = []

    # create window main
    window = tk.Tk()
    window.title("Convert PDF to PNG")
    window.rowconfigure(2, minsize=400)
    window.columnconfigure(2, minsize=70)

    # create frame body
    frm = tk.Frame(window)
    # title
    frm_title = tk.Frame(frm, height=20)
    lab = tk.Label(frm_title, text="To upload pdf files, press +", fg=hColor, font=('Helvetica 16 bold'))
    lab.pack()
    frm_title.grid(row=0, column=1, sticky=tk.N, pady=10)
    # buttons- files selected
    frm_names_item = tk.Frame(frm, height=50)
    frm_names_item.grid(row=1, column=1, sticky=tk.NS, pady=5)
    frm.grid(row=1, column=1)

    # create frame side
    frm_buttons = tk.Frame(window)
    # add file
    btn_add = tk.Button(frm_buttons, text="+", command=add_file, width=4, bg=bColor, fg=fColor,
                        font=('Helvetica 12 bold'))
    btn_add.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=10)
    # button send show only when choose files
    frm_buttons.grid(row=1, column=0, sticky=tk.NS, padx=30)

    # logo
    frm_image = tk.Frame(window)
    image = Image.open(f'logo.png')
    # f'client/logo.png'
    reSizeImage = image.resize((180, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(reSizeImage)
    label = tk.Label(frm_image, image=img)
    label.pack()
    frm_image.grid(row=0, column=1)

    window.mainloop()
