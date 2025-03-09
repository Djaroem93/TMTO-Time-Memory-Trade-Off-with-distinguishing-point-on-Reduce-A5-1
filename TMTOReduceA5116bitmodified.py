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

# Added missing function to convert uint to binary string
def uint_to_binstr(num, width):
    return format(num, f'0{width}b')

# Modified to use a51_reduced_enhanced instead of undefined generate_keystream_from_s_state
def generate_keystream_from_s_state(state):
    # Convert state to 16-bit binary string
    key = uint_to_binstr(state, 16)
    # Generate 16-bit keystream
    keystream = a51_reduced_enhanced(key, 16)
    # Convert keystream list to integer
    return int(''.join(map(str, keystream)), 2)

def main():
    with open('offlinetabledis1dgA5116bitmodified00000000.txt', 'w') as f:
        total = 0x10000  # 2^16
        for initial_state in range(total):
            # Tulis header initial state
            initial_bin = uint_to_binstr(initial_state, 16)
            f.write(f"Initial state = {initial_bin}\n")
            
            current_state = initial_state
            for step in range(1000):
                # Generate keystream
                keystream_uint = generate_keystream_from_s_state(current_state)
                keystream_bin = uint_to_binstr(keystream_uint, 16)
                
                # Tulis iterasi
                f.write(f"Iterasi {step+1} = {keystream_bin}\n")
                
                # Definisikan nilai distinguishing point
                distinguishing_point = int('00000000', 2)

                if (keystream_uint & 0xFFFF) == distinguishing_point:
                    f.write("DITEMUKAN DISTINGUISHING POINT\n")
                    break
                current_state = keystream_uint
            
            # Progress report
            if initial_state % 0x100 == 0:
                progress = (initial_state / total) * 100
                print(f"Progress: {progress:.2f}%")

if __name__ == "__main__":
    main()