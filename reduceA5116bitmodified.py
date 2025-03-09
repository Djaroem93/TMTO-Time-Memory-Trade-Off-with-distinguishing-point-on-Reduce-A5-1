def majority(a, b, c):
    return (a & b) | (a & c) | (b & c)

def a51_reduced_enhanced(key, num_bits):
    """Menghasilkan keystream dengan algoritma A5/1 versi reduced yang dimodifikasi."""
    # Validasi kunci 16-bit biner
    if len(key) != 16 or not all(c in '01' for c in key):
        raise ValueError("Kunci harus 16-bit biner (contoh: '0100100001111011')")
    
    # Inisialisasi LFSR dari kunci
    lfsr1 = [int(bit) for bit in key[:5]]    # 5-bit
    lfsr2 = [int(bit) for bit in key[5:12]]  # 7-bit
    lfsr3 = [int(bit) for bit in key[12:16]] # 4-bit
    
    # Langkah inisialisasi tambahan untuk mengacak state awal
    for _ in range(10):  # 10 iterasi inisialisasi
        cb1 = lfsr1[2]  # Clocking bit LFSR1 di posisi 3 (index 2)
        cb2 = lfsr2[4]  # Clocking bit LFSR2 di posisi 5 (index 4)
        cb3 = lfsr3[2]  # Clocking bit LFSR3 di posisi 3 (index 2)
        maj = majority(cb1, cb2, cb3)
        
        if cb1 == maj:
            # Feedback LFSR1: XOR lebih banyak bit (5, 4, 3, 2)
            feedback = lfsr1[4] ^ lfsr1[3] ^ lfsr1[2] ^ lfsr1[1]
            lfsr1 = [feedback] + lfsr1[:-1]
        
        if cb2 == maj:
            # Feedback LFSR2: XOR lebih banyak bit (7, 6, 5, 3)
            feedback = lfsr2[6] ^ lfsr2[5] ^ lfsr2[4] ^ lfsr2[2]
            lfsr2 = [feedback] + lfsr2[:-1]
        
        if cb3 == maj:
            # Feedback LFSR3: XOR lebih banyak bit (4, 3, 2, 1)
            feedback = lfsr3[3] ^ lfsr3[2] ^ lfsr3[1] ^ lfsr3[0]
            lfsr3 = [feedback] + lfsr3[:-1]
    
    # Menghasilkan keystream
    keystream = []
    for _ in range(num_bits):
        cb1 = lfsr1[2]
        cb2 = lfsr2[4]
        cb3 = lfsr3[2]
        maj = majority(cb1, cb2, cb3)
        
        if cb1 == maj:
            feedback = lfsr1[4] ^ lfsr1[3] ^ lfsr1[2] ^ lfsr1[1]
            lfsr1 = [feedback] + lfsr1[:-1]
        
        if cb2 == maj:
            feedback = lfsr2[6] ^ lfsr2[5] ^ lfsr2[4] ^ lfsr2[2]
            lfsr2 = [feedback] + lfsr2[:-1]
        
        if cb3 == maj:
            feedback = lfsr3[3] ^ lfsr3[2] ^ lfsr3[1] ^ lfsr3[0]
            lfsr3 = [feedback] + lfsr3[:-1]
        
        # Bit keystream dihitung dengan fungsi majority
        ks_bit = majority(lfsr1[-1], lfsr2[-1], lfsr3[-1])
        keystream.append(ks_bit)
    
    return keystream

# Contoh penggunaan
key = '0000000000000010'  # Kunci 16-bit semua nol
keystream = a51_reduced_enhanced(key, 16)
print("Keystream (bit pertama -> terakhir):", keystream)