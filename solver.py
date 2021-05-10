#!/usr/bin/env python3

import os
import json
import math
import string
import socket
import subprocess


def interact_remote(payload, address):
    output = ''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        sock.connect(address)

        sock.sendall(payload)
        
        while True:
            data = sock.recv(1024)

            if len(data) <= 0:
                break

            output += data

    return output


def interact_local(payload):
    filename = './deploy/service/ZN.Runner'

    with subprocess.Popen([filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
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
        

def counters_equal(counter1, counter2):
    eps = 100

    for x, y in zip(counter1, counter2):
        if abs(x - y) > eps:
            return False

    return True


def try_recover_flag(model, counters):
    flag = []

    for counter in counters:
        part = []

        for symbol in model:
            if counters_equal(model[symbol], counter):
                part.append(symbol)

        flag.append(part)

    return flag


def print_flag(flag):
    index = 0

    while True:
        line = ''

        for part in flag:
            if len(part) > index:
                line += part[index]
            else:
                line += ' '

        if set(line) == set(' '):
            break

        print(line)
        index += 1


def main():
    repeat = 1000
    alphabet = string.ascii_letters + string.digits + '{}_'

    model = get_model(alphabet, repeat)
    save_model(model)
    return
    model = load_model()
    
    write_flag('ZN{Qu4NtuM_H3ll0_w0RLD_2021}')

    counters = calculate_counters(repeat, interact_local)
    flag = try_recover_flag(model, counters)
    print_flag(flag)


if __name__ == '__main__':
    main()
