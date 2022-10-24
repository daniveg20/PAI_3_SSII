import socket
import ssl
import getpass
import time

inicio = time.time()

def gen_transacciones():
    for _ in range(300):
        usuario   = input("Nombre de Usuario: ")
        correo = input("Correo: ")
        try:
            x = getpass.getpass()
        except Exception as err:
            print('ERROR:', err)
        if "@" in correo:
            cadena = "el nombre de usuario es: " + str(usuario) + " ,su correo: " + str(correo) + " y su contraseña: " + str(x)
            break
        else:
            print("Ha escrito mal el correo")
    return cadena


file = open("./conf.txt", "r")
config = []
for line in file:
    line = line.strip()
    words = line.split("=")
    config.append(words[1])
num_pruebas = config[0]
file.close()

hostname = '127.0.0.1'

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations('./certchain.pem')
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
context.set_ciphers(cipher)
#for i in range(int(num_pruebas)):
cont = 0
for _ in range(int(num_pruebas)):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
        wrappedSocket.connect((hostname, 8443))
        if(cont==0):
            msgInput = gen_transacciones()   
            wrappedSocket.send(msgInput.encode())
            time.sleep(0.5)
            cont +=1
        msgInput1 = "Se establecio la conexion"
        wrappedSocket.send(msgInput1.encode())
        time.sleep(0.5)
print("\n")
final = time.time()

tiempoFinal = final - inicio
print(tiempoFinal)