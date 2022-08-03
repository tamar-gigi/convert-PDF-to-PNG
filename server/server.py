import shutil
import socket
import pickle
from savePDF.savePDF import savePDF
from convert.convert import convert
from threading import Thread, Lock


HOST = socket.gethostname()
PORT = 640
mutex = Lock()
numberThread = 0


def createThreadsClient(connectClient):
    global numberThread
    with connectClient:
        print(f"Connected by {address}")
        data = b""
        while True:
            binPdf = connectClient.recv(1024)
            if len(binPdf) < 1024:
                data += binPdf
                break
            data += binPdf
        files_obj = pickle.loads(data)
        mutex.acquire()
        routePdf = savePDF(files_obj, numberThread)
        images = convert(routePdf, numberThread)
        print(numberThread)
        shutil.rmtree(fr'savePDF/pdf_file/{numberThread}')
        shutil.rmtree(fr'convert/png_file/{numberThread}')
        numberThread += 1
        image_obj = pickle.dumps(images)

        mutex.release()
        print(len(image_obj))
        connectClient.sendall(pickle.dumps(len(image_obj)))
        connectClient.sendall(image_obj)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        try:
            serverSocket.bind((HOST, PORT))
        except socket.error as error:
            print(str(error))
        serverSocket.listen()
        while True:
            (clientSocket, address) = serverSocket.accept()
            t = Thread(target=createThreadsClient, args=(clientSocket,))
            t.start()
