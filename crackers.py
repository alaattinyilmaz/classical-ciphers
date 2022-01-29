import utils as crypto
import numpy as np
import sys

# Author: Emir Alaattin Yılmaz 2021

# Q1 Function
def crack_shift_cipher(cipher_text):
    ALPHABET_SIZE = len(crypto.uppercase)
    for shift_size in range(ALPHABET_SIZE):
        plaintext_candidate = ""
        for k in range(len(cipher_text)):
            shifted_letter = (crypto.uppercase[cipher_text[k]] + shift_size) % ALPHABET_SIZE
            plaintext_candidate = plaintext_candidate + crypto.inv_uppercase[shifted_letter]
        print("Plaintext: " , plaintext_candidate, " Key: " ,shift_size)

#Q2 Function

def crack_affine_cipher(cipher_text, alphabet, inv_alphabet, most_frequent_letter):
    class key(object):
        alpha=0
        beta=0
        gamma=0
        theta=0

    ALPHABET_SIZE = len(alphabet)

    decrypted_messages = []

    # Getting probable alpha values, it should be gcd(alpha,ALPHABET_SIZE)=1
    alpha_space = []
    for k in range(ALPHABET_SIZE):
        if(crypto.modinv(k, ALPHABET_SIZE) != None):
            alpha_space.append(k)

    # alpha_space for english alphabet: [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    # Getting frequencies of letters in ciphertext
    frequencies = dict()
    for k in range(len(cipher_text)):
        if(cipher_text[k] in frequencies):
            frequencies[cipher_text[k]] += 1
        elif(cipher_text[k] == ' '):
            continue
        else:
            frequencies[cipher_text[k]] = 1

    most_frequent_cipher_letter = max(frequencies, key=frequencies.get)
    predicted_beta = (alphabet[most_frequent_cipher_letter] - alphabet[most_frequent_letter]) % ALPHABET_SIZE

    keys = []
    for alpha_i in alpha_space:
        key.alpha = alpha_i
        key.beta = predicted_beta
        key.gamma = crypto.modinv(key.alpha, ALPHABET_SIZE) # you can compute decryption key from encryption key
        key.theta = ALPHABET_SIZE-(key.gamma*key.beta) % ALPHABET_SIZE
        dtext = crypto.Affine_Dec(cipher_text, key, alphabet, inv_alphabet)
        #print(dtext)
        decrypted_messages.append(dtext)
        save_key = key()
        save_key.alpha, save_key.beta, save_key.gamma, save_key.theta = key.alpha, key.beta, key.gamma, key.theta
        keys.append(save_key)

    return decrypted_messages, keys
    
    # PLAINTEXT: "ANYBODY CAN MAKE HISTORY. ONLY A GREAT MAN CAN WRITE IT."

# Q7 Functions

myalphabet = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13,
'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25,
'.':26, ' ':27}

inv_myalphabet = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 
12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 
25: 'Z', 26: '.', 27: ' '}

def Affine_Dec_Bigram(ptext, key, alphabet, inv_alphabet):
    plen = len(ptext)
    ctext = ''
    ALPHABET_SIZE = len(alphabet)
    for i in range (0, plen, 2):
        letter = ptext[i] + ptext[i+1]
        if letter in alphabet:
            poz = alphabet[letter]
            poz = (key.gamma*poz+key.theta) % ALPHABET_SIZE
            ctext += inv_alphabet[poz]
        else:
            ctext += ptext[i]
    return ctext

def crack_affine_cipher_bigram(cipher_text, alphabet):

    print("\n CIPHERTEXT: \n",cipher_text)

    bigrams = dict()

    ALPHABET_SIZE = len(alphabet)

    for l1 in alphabet.keys():
        for l2 in alphabet.keys():
            two_letter = l1+l2
            bigrams[two_letter] = alphabet[l1]*ALPHABET_SIZE + alphabet[l2]

    inv_bigrams = dict()

    for k in bigrams.keys():
        inv_bigrams[bigrams[k]] = k

    class key(object):
        alpha=0
        beta=0
        gamma=0
        theta=0

    # bigrams['.X'] : 751, bigrams['BE'] : 32
    BIGRAM_ALPHABET_SIZE = len(bigrams)

    alpha_space = []
    for a in range(BIGRAM_ALPHABET_SIZE):
        if(crypto.modinv(a, BIGRAM_ALPHABET_SIZE) != None):
            alpha_space.append(a)

    for alpha_i in alpha_space:
        key.alpha = alpha_i
        predicted_beta = (32 - 751 * key.alpha) % BIGRAM_ALPHABET_SIZE
        key.beta = predicted_beta
        key.gamma = crypto.modinv(key.alpha, BIGRAM_ALPHABET_SIZE) # you can compute decryption key from encryption key
        key.theta = (BIGRAM_ALPHABET_SIZE-(key.gamma*key.beta)) % BIGRAM_ALPHABET_SIZE
        dtext = Affine_Dec_Bigram(cipher_text, key, bigrams, inv_bigrams)

        if("IT DOES "in dtext):
            print("\n PLAINTEXT: \n", dtext)
            print("\n ENC KEY (alpha,beta): ", (key.alpha, key.beta))
            print("\n DEC KEY (gamma,theta): ", (key.gamma, key.theta), "\n")

    # PLAINTEXT: IT DOES NOT DO TO DWELL ON DREAMS AND FORGET TO LIVE.X

# Q8 Function

def crack_vigenere_cipher(cipher_text):

    ALPHABET_SIZE = len(crypto.uppercase)

    print("\n CIPHERTEXT: \n \n",cipher_text)

    # First find the key length

    # Setting a maximum key length to try, I set as 20.
    maximum_key_length = 20

    # Cleaning punctuations and blanks first of ciphertext

    clean_ciphertext = ''.join(e for e in cipher_text if e.isalnum())
    clean_ciphertext = clean_ciphertext.lower()

    # Shifting text one by one to right and collect them

    filler_text = ''.join([' ' for k in range(len(clean_ciphertext))])
    shifted_texts = []

    for i in range(maximum_key_length):
        shifted_text = filler_text[len(clean_ciphertext)-i : ] + clean_ciphertext[0 : len(clean_ciphertext)-i] 
        shifted_texts.append(shifted_text)

    coincidences = dict()

    # Counting the coincidences with ciphertext and shifted texts one by one
    for i,sht in enumerate(shifted_texts):
        coincidences[i] = 0
        for j,ch in enumerate(sht):
            if(clean_ciphertext[j]==sht[j]):
                coincidences[i] += 1
                
    coincidences[0] = -1

    print("\n COINCIDENCES: \n \n",coincidences)

    # Coincidences have jumps on 5, 10, 15, shifts but I am taking the maximum with programmatically
    most_frequent_cipher_letter = max(coincidences, key=coincidences.get)

    print("\n Most Frequent Coincidence Shift: ",most_frequent_cipher_letter, " Count: ",coincidences[most_frequent_cipher_letter])

    print("\n Key length: ",most_frequent_cipher_letter)

    # Creating sub_ciphers by taking 0th, 15th, 30th,... - 1th 16th 31th ... -  letters and etc.
    sub_ciphers = []

    key_length = most_frequent_cipher_letter

    for k in range(key_length):
        sub_cipher = ""
        for m in range(k,len(clean_ciphertext),key_length):
            sub_cipher = sub_cipher + clean_ciphertext[m]

        sub_ciphers.append(sub_cipher)

    # Letter frequencies in English
    A = crypto.letter_frequencies
    # Getting sub-cipher letter frequencies
    letter_freqs = []

    for sc in sub_ciphers:
        letter_freq = dict()
        total_letter_sc = len(sc)

        for ch in sc:
            if ch in letter_freq:
                letter_freq[ch] += 1
            else:
                letter_freq[ch] = 1
        
        for other_letter in crypto.lowercase.keys():
            if (other_letter not in letter_freq):
                letter_freq[other_letter] = 0 # This letter not occured in this sub-cipher

        for k in letter_freq.keys():
            letter_freq[k] = round(letter_freq[k] / total_letter_sc, 4)

        letter_freq = dict(sorted(letter_freq.items(), key=lambda item: item[0])) # Sort by keys -> a, b, c ...
        letter_freqs.append(letter_freq)

    # Predicting key by dot product with shifted A (english letter frequencies), largest value is the most probable shift amount
    key_vigenere = ""
    for lf in letter_freqs:
        lf_freq_i = list(lf.values())
        sub_cipher_dot_frequencies = []
        for shift_amount in range(0,ALPHABET_SIZE): 
            shifted_A = np.roll(A,shift_amount)
            sub_cipher_dot_frequencies.append(round(np.dot(lf_freq_i, shifted_A),4))
        
        most_probable_shift_amount = sub_cipher_dot_frequencies.index(max(sub_cipher_dot_frequencies))
        #print(sub_cipher_dot_frequencies)
        key_vigenere = key_vigenere + crypto.inv_lowercase[most_probable_shift_amount]

    print("\n KEY: ",key_vigenere)

    # key_vigenere = "hayao"
    # Decrypting the ciphertext by use of key
    plaintext_candidate = ""
    punc_counter = 0

    for c,ch in enumerate(cipher_text):
        
        letter = cipher_text[c]
        
        if (letter.isupper()):
            alphabet_type = crypto.uppercase
            inv_alphabet_type = crypto.inv_uppercase
        elif (letter.islower()):
            alphabet_type = crypto.lowercase
            inv_alphabet_type = crypto.inv_lowercase
        else:
            plaintext_candidate = plaintext_candidate + letter
            punc_counter += 1
            continue
        
        shift_size = crypto.lowercase[key_vigenere[(c - punc_counter) % len(key_vigenere)]]
        
        shifted_letter = (alphabet_type[letter] - shift_size + ALPHABET_SIZE) % ALPHABET_SIZE
        plaintext_candidate = plaintext_candidate + inv_alphabet_type[shifted_letter]

    print("\n PLAINTEXT: \n \n ",plaintext_candidate)

    # PLAINTEXT: But there is one way in this country in which all men are created equal-there is one human institution that makes a pauper the equal of a Rockefeller, the stupid man the equal of an Einstein, and the ignorant man the equal of any college president. That institution, gentlemen, is a court. It can be the Supreme Court of the United Etates or the humblest J.P court in the land, or this honorable court which you serve. Our courts have their faults, as does any human institution, but in this country our courts are the great levelers, and in our courts all men are created equal. I'm no idealist to believe firmly in the integrity of our courts and in the jury-system that is no ideal to me, it is a living, working reality. Gentlemen, a court is no better than each man of you sitting before me on this jury. A court is only as sound as its jury, and a jury is only as sound as the men who make it up. I am confident that you gentlemen will review without passion the evidence you have heard, come to a decision, and restore this defendant to his family. In the name of God, do your duty.

if __name__ == '__main__':

    quests = sys.argv
    if(len(quests) == 2):
        quest = str(sys.argv[1])
        if(quest == "sc"):
            # Q1:
            print("\n SHIFT CIPHER \n")
            cipher_text_q1 = "NKWZ"
            crack_shift_cipher(cipher_text_q1)
        
        elif(quest == "ac"):
            # Q2:
            print("\n AFFINE CIPHER \n")
            cipher_text_q2 = "REZANSZ JRE VRDB CLXGNOZ. NEMZ R TOBRG VRE JRE HOLGB LG."
            decrypted_messages, keys = crack_affine_cipher(cipher_text_q2, crypto.uppercase, crypto.inv_uppercase, 'A')
            for d,key in zip(decrypted_messages,keys):
                print(d, "\n Enc Key (alpha,beta): " , (key.alpha, key.beta),"\n Dec Key (gamma,tetha): " , (key.gamma, key.theta))
        
        elif(quest == "bac"):   
            # Q7:
            print("\n BIGRAM AFFINE CIPHER")
            cipher_text_q7 = "RYHUHBCMNHLMHHUYWMNXDIXMR.HUGB RCMD.HMZHOTJYUYWMZJOBBE"
            crack_affine_cipher_bigram(cipher_text_q7, myalphabet)

        elif(quest == "vc"):
            # Q8:
            print("\n VIGENERE CIPHER \n")
            cipher_text_q8 = "Iur tvlrc ig vnc wof il tvps aoiutpy wu wfiqo ajl aln yrs jrcahld cqihl-rhsye gs cue fuahn gngairuhpol tvht kayls y pobpcr hoe cqihl mf o Yoaksmejlsy, tfe gaunir tal tvl eouos od ab Lilshlil, abk tfe wnnmrout kab ahc eebaj ot hnw ccslcgs wrcswkelt. Hoar ibztgtiaimn, ulnrlstel, ig h cmufa. Ir cou bc tvl Sspflmc Ccbrr ot ahc Ubptcd Saareg vr rhs oukbzlsr J.D josrh pn rhs sald, cy tfig oolofhbje qvupt koiah mvu qefce. Muf josrhz hyvs ahcif maslhz, aq dcls ynm oukab pnqtwauricu, bst wu tfig josnhyy muf josrhz ape hoe ersht jejllcrg, hnb ib vup ccbrrs osl keb hrc cflarer lqsaz. P'm lo wkeylwzt ro pllgejl fgrasy gn hoe gnhlgpihf od oiy cmufas ynr pn rhs qupy-gfsrea ahyt wz nm irlaj tc te, gt wz a jijpne, wcykgnu yeylway. Eebalcmsu, a aoiyt gs bv bcthlr rhou eycv tal ot fos swatgnu iedofl mc ob ahgs xbrw. A qvupt wz ollm hs qoiud ys was huff, ald o qupy wz ollm hs qoiud ys hoe keb dhm more gt iw. I ym qvndirlnr tvht woi neltzlmcn kplj rscicw kptfoia pysgpol tvl etirlnae mvu fajl hcafk, cmms ao y dsjiqicu, ald flsrofl tfig kedebkalt hv hgs thmglm. Pn rhs uake cm Gmd, rv ymuf kury."
            crack_vigenere_cipher(cipher_text_q8)

        else:
            print("Not a valid argument (argument values: q1,q2,q7,q8)")
    else:
        print("Please enter the question as an argument: q1,q2,q7,q8")