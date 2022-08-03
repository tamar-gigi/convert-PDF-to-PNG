from pdf2image import convert_from_path
import multiprocessing
import os


def poolPage(file, path, index, page, newPDF):
    path1 = f'{path}/{index}_{os.path.splitext(os.path.basename(file))[0]}.png'
    page.save(f'{path1}')
    with open(f'{path1}', 'rb') as image:
        binImage = image.read()
    newPDF.append([os.path.basename(path1), binImage])


def poolPdf(file, path, poppler_path, newPDF):
    pages = convert_from_path(pdf_path=f'{file}', dpi=500, poppler_path=poppler_path)

    p_arr = []
    for index, page in enumerate(pages):
        p = multiprocessing.Process(target=poolPage, args=(file, path, index, page, newPDF))
        p_arr.append(p)
    for p in p_arr:
        p.start()
    for p in p_arr:
        p.join()


def convert(files, numberThread):
    path = f'convert/png_file/{numberThread}'
    os.mkdir(f'{path}')
    poppler_path = r'convert/poppler-0.68.0_x86/poppler-0.68.0/bin'
    ret_list = []
    with multiprocessing.Manager() as manager:
        newPDF = manager.list()
        p_arr = []
        for file in files:
            p = multiprocessing.Process(target=poolPdf, args=(file, path, poppler_path, newPDF))
            p_arr.append(p)
        for p in p_arr:
            p.start()
        for p in p_arr:
            p.join()
        ret_list = list(newPDF)
    return ret_list
