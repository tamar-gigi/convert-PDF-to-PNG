import os

from reportlab.pdfgen import canvas
import multiprocessing


def poolPDF(file, name, res):
    path = fr"{name}/{file[0]}"
    my_canvas = canvas.Canvas(path)
    my_canvas.drawString(0, 0, '')
    my_canvas.save()
    with open(path, 'wb') as pdf:
        pdf.write(file[1])
    res.append(path)


def savePDF(files, numberThread):
    path = f'savePDF/pdf_file/{numberThread}'
    os.mkdir(f'{path}')
    res = []
    with multiprocessing.Manager() as manager:
        newImage = manager.list()
        p_arr = []
        for file in files:
            p = multiprocessing.Process(target=poolPDF, args=(file, path, newImage))
            p_arr.append(p)
        for p in p_arr:
            p.start()
        for p in p_arr:
            p.join()
        res = list(newImage)
    return res
