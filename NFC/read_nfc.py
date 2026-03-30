from smartcard.System import readers
import time

def _connect():
    r = readers()
    if not r:
        print("[ERROR] No NFC reader found!")
        exit(1)
        
    print("Readers:", r)
    
    conn = r[0].createConnection()
    conn.connect()
    
    return conn

def _connect():
    r = readers()
    if not r:
        raise RuntimeError("No NFC readers found")
    conn = r[0].createConnection()
    conn.connect()
    return conn

from smartcard.System import readers

def _connect():
    r = readers()
    if not r:
        raise RuntimeError("No NFC readers found")
    conn = r[0].createConnection()
    conn.connect()
    return conn

def read_page(conn, page):
    READ = [0xFF, 0xB0, 0x00, page, 0x04]
    data, sw1, sw2 = conn.transmit(READ)
    return data

def test_tag():
    conn = _connect()

    print("\n=== BASIC INFO ===")
    # Read UID (pages 0–2)
    uid = read_page(conn, 0) + read_page(conn, 1)[:3]
    print("UID:", uid)

    # Capability Container (page 3)
    cc = read_page(conn, 3)
    print("CC (Capability Container):", cc)

    # Memory size from CC byte 2
    # For NTAG215, CC[2] = 0x6D (109 blocks * 8 bytes = 868 bytes)
    if cc[2] == 0x6D:
        print("Detected: NTAG215 (confirmed by CC)")
    elif cc[2] == 0x12:
        print("Detected: NTAG213")
    elif cc[2] == 0x3E:
        print("Detected: NTAG216")
    else:
        print("Unknown tag type — CC byte:", hex(cc[2]))

    print("\n=== FIRST 50 PAGES ===")
    pages = []
    for p in range(0, 50):
        data = read_page(conn, p)
        pages.append(data)
        print(f"Page {p:02d}: {data}")

    print("\n=== LOCK BYTES ===")
    print("Static lock bytes (page 2):", pages[2])
    print("Dynamic lock bytes (page 40):", pages[40] if len(pages) > 40 else "Not available")

    print("\n=== NDEF RAW DATA (pages 4–12) ===")
    raw = []
    for p in range(4, 12):
        raw += pages[p]
    print(raw)

    print("\n=== NDEF PARSE ATTEMPT ===")
    try:
        if raw[0] != 0x03:
            print("No NDEF TLV found")
            return

        ndef_len = raw[1]
        print("NDEF length:", ndef_len)

        record = raw[2:2+ndef_len]
        print("Record bytes:", record)

        payload_len = record[2]
        lang_len = record[4]

        print("Payload length:", payload_len)
        print("Language code length:", lang_len)

        text_start = 5 + lang_len
        text_bytes = record[text_start:text_start + (payload_len - 1 - lang_len)]

        text = ''.join(chr(b) for b in text_bytes)
        print("Decoded text:", text)

    except Exception as e:
        print("Error parsing NDEF:", e)

    print("\n=== END OF TEST ===\n")

def write_text(text: str):
    conn = _connect()

    text_bytes = [ord(c) for c in text]
    lang = [0x65, 0x6E]  # "en"
    lang_len = len(lang)

    # Payload = status + lang + text
    payload_len = 1 + lang_len + len(text_bytes)

    # NDEF length = header + type + payload_len + type byte + payload
    # PLUS the terminator (FE)
    ndef_len = 3 + payload_len + 1

    ndef = [
        0x03, ndef_len,       # NDEF TLV
        0xD1,                 # MB/ME/SR/TNF
        0x01,                 # Type length
        payload_len,          # Payload length
        0x54,                 # 'T' (Text record)
        lang_len              # Status byte: language code length
    ] + lang + text_bytes + [
        0xFE                  # Terminator TLV
    ]

    # Write starting at page 4
    page = 4
    for i in range(0, len(ndef), 4):
        chunk = ndef[i:i+4]
        while len(chunk) < 4:
            chunk.append(0x00)

        WRITE = [0xFF, 0xD6, 0x00, page, 0x04] + chunk
        conn.transmit(WRITE)
        page += 1

    print(f"Written text: {text}")



def read_text() -> str:
    """Read an NDEF Text Record from an NTAG tag and return the text."""
    conn = _connect()

    def read_page(page):
        READ = [0xFF, 0xB0, 0x00, page, 0x04]
        data, sw1, sw2 = conn.transmit(READ)
        return data

    # Read a reasonable chunk of pages
    raw = []
    for p in range(4, 20):
        raw += read_page(p)

    # Parse NDEF TLV
    i = 0
    if raw[i] != 0x03:
        raise RuntimeError("No NDEF TLV found")

    length = raw[i+1]
    record = raw[i+2:i+2+length]

    # Parse NDEF Text Record
    payload_len = record[2]
    lang_len = record[4]
    text_start = 5 + lang_len
    text_bytes = record[text_start:text_start + payload_len - 1 - lang_len]

    return ''.join(chr(b) for b in text_bytes)


# Main / start of run loop

# while True:
#     try:
#         # connection = r[0].createConnection()
#         # connection.connect()
        
#         # # APDU to get UID (works for most MIFARE tags)
#         # GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        
#         # data, sw1, sw2 = connection.transmit(GET_UID)
        

#         # print("UID:", data)
#         # print("Status:", hex(sw1), hex(sw2))
        
#         # test_tag()
#         write_text("01A-1250")
#         value = read_text()
#         print("Read from tag:", value)
#     except:
#         print("There was no NFC chip found!")
        
#     print('-'*50)
        
    # time.sleep(5)
    # exit(0)
