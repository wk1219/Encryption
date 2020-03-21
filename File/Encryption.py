import list
import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_file, out_file=None, chunksize=64*1024):
    if not out_file:
        out_file = in_file + '.ark'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_file)

    with open(in_file, 'rb') as infile:
        with open(out_file, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_file, out_file=None, chunksize=24*1024):
    if not out_file:
        out_file = os.path.splitext(in_file)[0]

    with open(in_file, 'rb') as infile:
        origin_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origin_size)


def AllEncrypt(flist, key):
    for i in range (0, len(flist)):
        if (os.path.isfile(flist[i])):
            print('Encrypting >> ' + flist[i])
            encrypt_file(key, flist[i])
            os.remove(flist[i])

def AllDecrypt(flist, key):
    for i in range (0, len(flist)):
        if (os.path.isfile(flist[i])):
            fname, ext = os.path.splitext(flist[i])
            if(ext == '.ark'):
                print('Decrypting >> ' + flist[i])
                decrypt_file(key, flist[i])
                os.remove(flist[i])

def Path():
    flist = []
    path = input("Input >> ")
    flist = list.file_list(path)
    return flist

def KeyGenerator():
    key = input("Input Key (16 characters) >> ")
    en_key = key.encode('utf-8')
    return en_key


files = Path()
key = KeyGenerator()
print(type(key))
# AllEncrypt(files, key)
# AllDecrypt(files, key)
