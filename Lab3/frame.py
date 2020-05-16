import sys


def frame(data):
    separator = '01111110'
    count = 0
    data = str(data)
    stuffed = separator
    for i in data:
        if count == 5:
            count = 1
            stuffed = stuffed + '0' + i

        elif count <= 4:
            if i == '1':
                count = count + 1
                stuffed = stuffed + i

            elif i == '0':
                count = 0
                stuffed = stuffed + i

    stuffed = stuffed + separator
    return stuffed


def unframe(data):
    non_stuffed = ''
    count = 0
    for i in data:

        if count == 5:
            if i == '0':
                count = 0
            elif i == '1':
                count = count + 1
                non_stuffed = non_stuffed + i

        elif count == 6:
            if i == '1':
                print("Transmission Error")
            elif i == '0':
                non_stuffed = non_stuffed[:len(non_stuffed) - 7]
                count = 0
        elif count <= 4:
            if i == '1':
                count = count + 1
                non_stuffed = non_stuffed + i
            elif i == '0':
                count = 0
                non_stuffed = non_stuffed + i

    return non_stuffed


def encode(data, file):
    remainder = crc(data)
    data = data + remainder
    data_framed = frame(data)
    with open(file, 'w') as file_out:
        file_out.write(data_framed)


def decode(data, file):
    non_framed_data = unframe(data)
    remainder = crc(non_framed_data)
    if remainder == '000':
        with open(file, 'w') as file_out:
            file_out.write(non_framed_data[:-3])
    else:
        print("Invalid checksum!")


def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def crc(data):
    key = '1001'
    data = data + '0' * (len(key) - 1)
    pick = len(key)
    tmp = data[0: pick]

    while pick < len(data):
        if tmp[0] == '1':
            tmp = xor(key, tmp) + data[pick]
        else:
            tmp = xor('0' * pick, tmp) + data[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(key, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    remainder = tmp
    return remainder


def main():
    if len(sys.argv) < 4:
        print("Not enough arguments!")

    if sys.argv[1] == '--encode':
        with open(sys.argv[2], 'r') as file_in:
            data = file_in.read()
            encode(data, sys.argv[3])
    elif sys.argv[1] == '--decode':
        with open(sys.argv[2], 'r') as file_out:
            data = file_out.read()
            decode(data, sys.argv[3])


if __name__ == '__main__':
    main()
