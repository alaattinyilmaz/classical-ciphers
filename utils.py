import math

# This is method to compute Euler's function, not good for big numbers
def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

# The extended Euclidean algorithm (EEA)
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

# Modular inverse algorithm that uses EEA
def modinv(a, m):
    if a < 0:
        a = m+a
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

# You can use the the following variables for encoding an decoding of English letters    
lowercase = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8,
         'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16,
         'r':17, 's':18,  't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24,
         'z':25}

uppercase = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8,
         'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16,
         'R':17, 'S':18,  'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24,
         'Z':25}

inv_lowercase = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i',
         9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 15:'p', 16:'q',
         17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y',
         25:'z'}

inv_uppercase = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',
                 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P',
                 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X',
                 24:'Y', 25:'Z'}

letter_count = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0,
         'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0,
         'R':0, 'S':0,  'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}

# Letter frequencies in English
letter_frequencies = [0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.0236,0.0015,0.01974,0.00074]

# Turkish texts
turkish_alphabet = {'A':0, 'B':1, 'C':2, 'Ç':3, 'D':4, 'E':5, 'F':6, 'G':7, 'Ğ':8, 'H':9, 'I':10, 'İ': 11, 'J':12, 'K':13,
'L':14, 'M':15, 'N':16, 'O':17, 'Ö':18, 'P':19, 'R':20, 'S':21, 'Ş':22, 'T':23, 'U':24, 'Ü':25,
'V':26, 'Y':27, 'Z':28, '.':29, ',':30}

inv_turkish_alphabet = {0: 'A', 1: 'B', 2: 'C', 3: 'Ç', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'Ğ', 9: 'H', 10: 'I', 11: 'İ', 
12: 'J', 13: 'K', 14: 'L', 15: 'M', 16: 'N', 17: 'O', 18: 'Ö', 19: 'P', 20: 'R', 21: 'S', 22: 'Ş', 23: 'T', 24: 'U', 25: 'Ü',
 26: 'V', 27: 'Y', 28: 'Z', 29: '.', 30: ','}

# Affine cipher encryption and decryption routines: REVISITED for all languages by Emir Alaattin Yılmaz
def Affine_Enc(ptext, key, alphabet, inv_alphabet):
    plen = len(ptext)
    ctext = ''
    ALPHABET_SIZE = len(alphabet)
    for i in range (0,plen):
        letter = ptext[i]
        if letter in alphabet:
            poz = alphabet[letter]
            poz = (key.alpha*poz+key.beta) % ALPHABET_SIZE
            ctext += inv_alphabet[poz]
        else:
            ctext += ptext[i]
    return ctext

def Affine_Dec(ctext, key, alphabet, inv_alphabet):
    plen = len(ctext)
    ptext = ''
    ALPHABET_SIZE = len(alphabet)
    for i in range (0,plen):
        letter = ctext[i]
        if letter in alphabet:
            poz = alphabet[letter]
            poz = (key.gamma*poz+key.theta) % ALPHABET_SIZE
            ptext += inv_alphabet[poz]
        else:
            ptext += ctext[i]
    return ptext
