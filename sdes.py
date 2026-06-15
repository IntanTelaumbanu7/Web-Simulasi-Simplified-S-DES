class SDES:
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]

    S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 2],
        [2, 1, 0, 3]
    ]

    @staticmethod
    def to_bits(text):
        return [int(ch) for ch in text]

    @staticmethod
    def to_str(bits):
        return ''.join(str(bit) for bit in bits)

    @staticmethod
    def xor(a, b):
        return [x ^ y for x, y in zip(a, b)]

    @staticmethod
    def left_shift(bits, n):
        return bits[n:] + bits[:n]

    @staticmethod
    def permute(bits, table):
        return [bits[i - 1] for i in table]

    @staticmethod
    def validate_bits(value, length, label):
        if len(value) != length or any(ch not in '01' for ch in value):
            raise ValueError(f'{label} harus tepat {length} bit biner dan hanya berisi 0 atau 1.')

    @staticmethod
    def bit_cells(value):
        return list(value)

    @staticmethod
    def make_table(title, headers, rows, note=''):
        """Membentuk data tabel agar tampilan mirip contoh perhitungan S-DES."""
        return {
            'title': title,
            'headers': headers,
            'rows': [{'label': label, 'bits': list(bits)} for label, bits in rows],
            'note': note
        }

    def generate_keys(self, key_text):
        self.validate_bits(key_text, 10, 'Kunci')
        key = self.to_bits(key_text)
        p10 = self.permute(key, self.P10)
        left = p10[:5]
        right = p10[5:]
        ls1_left = self.left_shift(left, 1)
        ls1_right = self.left_shift(right, 1)
        k1 = self.permute(ls1_left + ls1_right, self.P8)
        ls2_left = self.left_shift(ls1_left, 2)
        ls2_right = self.left_shift(ls1_right, 2)
        k2 = self.permute(ls2_left + ls2_right, self.P8)

        key_str = key_text
        p10_str = self.to_str(p10)
        ls1_str = self.to_str(ls1_left + ls1_right)
        ls2_str = self.to_str(ls2_left + ls2_right)
        k1_str = self.to_str(k1)
        k2_str = self.to_str(k2)

        return {
            'original_key': key_str,
            'p10_result': p10_str,
            'left_part': self.to_str(left),
            'right_part': self.to_str(right),
            'after_ls1_left': self.to_str(ls1_left),
            'after_ls1_right': self.to_str(ls1_right),
            'k1': k1_str,
            'after_ls2_left': self.to_str(ls2_left),
            'after_ls2_right': self.to_str(ls2_right),
            'k2': k2_str,
            'k1_table': self.make_table(
                'Tabel Pembangkitan K1',
                [str(i) for i in range(1, 11)],
                [
                    ('K', key_str),
                    ('P10(K)', p10_str),
                    ('Shift(P10(K))', ls1_str),
                    ('P8(Shift(P10(K))) = K1', k1_str),
                ],
                'K1 diperoleh dari P10, LS-1, lalu P8.'
            ),
            'k2_table': self.make_table(
                'Tabel Pembangkitan K2',
                [str(i) for i in range(1, 11)],
                [
                    ('K', key_str),
                    ('P10(K)', p10_str),
                    ('Shift³(P10(K))', ls2_str),
                    ('P8(Shift² setelah LS-1)) = K2', k2_str),
                ],
                'K2 diperoleh dari hasil LS-1 yang digeser lagi 2 kali, lalu P8.'
            ),
            '_k1_bits': k1,
            '_k2_bits': k2,
        }

    def sbox(self, four_bits, box):
        row = (four_bits[0] << 1) | four_bits[3]
        col = (four_bits[1] << 1) | four_bits[2]
        value = box[row][col]
        output = [(value >> 1) & 1, value & 1]
        return output, row, col, value

    def round_function(self, right, subkey, key_name):
        ep = self.permute(right, self.EP)
        xor_key = self.xor(ep, subkey)
        left4 = xor_key[:4]
        right4 = xor_key[4:]
        s0_out, s0_row, s0_col, s0_val = self.sbox(left4, self.S0)
        s1_out, s1_row, s1_col, s1_val = self.sbox(right4, self.S1)
        sbox_combined = s0_out + s1_out
        p4 = self.permute(sbox_combined, self.P4)

        right_str = self.to_str(right)
        ep_str = self.to_str(ep)
        subkey_str = self.to_str(subkey)
        xor_str = self.to_str(xor_key)
        sbox_str = self.to_str(sbox_combined)
        p4_str = self.to_str(p4)

        return {
            'key_name': key_name,
            'right_input': right_str,
            'subkey': subkey_str,
            'ep_result': ep_str,
            'xor_with_key': xor_str,
            'sbox0_input': self.to_str(left4),
            'sbox1_input': self.to_str(right4),
            'sbox0_row': s0_row,
            'sbox0_col': s0_col,
            'sbox0_value': s0_val,
            'sbox1_row': s1_row,
            'sbox1_col': s1_col,
            'sbox1_value': s1_val,
            'sbox0_output': self.to_str(s0_out),
            'sbox1_output': self.to_str(s1_out),
            'sbox_combined': sbox_str,
            'p4_result': p4_str,
            'function_table': self.make_table(
                f'Tabel Fungsi F dengan {key_name}',
                [str(i) for i in range(1, 9)],
                [
                    ('R', right_str),
                    ('E/P(R)', ep_str),
                    (key_name, subkey_str),
                    (f'E/P(R) ⊕ {key_name}', xor_str),
                    ('SBoxes', sbox_str),
                    ('P4(SBoxes)', p4_str),
                ],
                'SBoxes adalah gabungan output S0 dan S1 sebelum dipermutasi P4.'
            ),
            '_p4_bits': p4,
        }

    def process(self, input_text, key_text, mode='encrypt'):
        self.validate_bits(input_text, 8, 'Plaintext/Ciphertext')
        self.validate_bits(key_text, 10, 'Kunci')
        mode = mode if mode in ('encrypt', 'decrypt') else 'encrypt'
        key_steps = self.generate_keys(key_text)
        k1 = key_steps['_k1_bits']
        k2 = key_steps['_k2_bits']
        round1_key = k1 if mode == 'encrypt' else k2
        round2_key = k2 if mode == 'encrypt' else k1
        round1_key_name = 'K1' if mode == 'encrypt' else 'K2'
        round2_key_name = 'K2' if mode == 'encrypt' else 'K1'

        bits = self.to_bits(input_text)
        ip = self.permute(bits, self.IP)
        l0 = ip[:4]
        r0 = ip[4:]

        rf1 = self.round_function(r0, round1_key, round1_key_name)
        l1 = self.xor(l0, rf1['_p4_bits'])
        r1 = r0
        sw_left = r1
        sw_right = l1

        rf2 = self.round_function(sw_right, round2_key, round2_key_name)
        l2 = self.xor(sw_left, rf2['_p4_bits'])
        r2 = sw_right
        combined = l2 + r2
        output_bits = self.permute(combined, self.IP_INV)
        output = self.to_str(output_bits)

        ip_str = self.to_str(ip)
        combined_str = self.to_str(combined)

        # Remove internal bit arrays before returning to template
        for d in (key_steps, rf1, rf2):
            for internal in list(d.keys()):
                if internal.startswith('_'):
                    del d[internal]

        return {
            'mode': mode,
            'mode_label': 'Enkripsi' if mode == 'encrypt' else 'Dekripsi',
            'input_label': 'Plaintext' if mode == 'encrypt' else 'Ciphertext',
            'output_label': 'Ciphertext' if mode == 'encrypt' else 'Plaintext',
            'input': input_text,
            'key': key_text,
            'output': output,
            'key_generation': key_steps,
            'initial_permutation': {
                'input': input_text,
                'ip_result': ip_str,
                'left': self.to_str(l0),
                'right': self.to_str(r0),
                'table': self.make_table(
                    'Tabel Initial Permutation',
                    [str(i) for i in range(1, 9)],
                    [
                        ('Input', input_text),
                        ('IP(Input)', ip_str),
                    ],
                    'Hasil IP kemudian dibagi menjadi L0 dan R0.'
                ),
            },
            'round1': {
                'title': 'Round Function 1',
                'key_name': round1_key_name,
                'left_input': self.to_str(l0),
                'right_input': self.to_str(r0),
                'function': rf1,
                'left_output': self.to_str(l1),
                'right_output': self.to_str(r1),
                'combined_before_swap': self.to_str(l1 + r1),
                'xor_table': self.make_table(
                    'Tabel XOR Bagian Kiri Round 1',
                    [str(i) for i in range(1, 5)],
                    [
                        ('L0', self.to_str(l0)),
                        (f'F(R0,{round1_key_name})', rf1['p4_result']),
                        ('L1', self.to_str(l1)),
                    ],
                    'L1 = L0 ⊕ F(R0, subkey).'
                ),
            },
            'swap': {
                'before_left': self.to_str(l1),
                'before_right': self.to_str(r1),
                'after_left': self.to_str(sw_left),
                'after_right': self.to_str(sw_right),
                'table': self.make_table(
                    'Tabel Swap',
                    [str(i) for i in range(1, 9)],
                    [
                        ('Sebelum SW', self.to_str(l1) + self.to_str(r1)),
                        ('Setelah SW', self.to_str(sw_left) + self.to_str(sw_right)),
                    ],
                    'Swap menukar posisi kiri dan kanan.'
                ),
            },
            'round2': {
                'title': 'Round Function 2',
                'key_name': round2_key_name,
                'left_input': self.to_str(sw_left),
                'right_input': self.to_str(sw_right),
                'function': rf2,
                'left_output': self.to_str(l2),
                'right_output': self.to_str(r2),
                'combined': combined_str,
                'xor_table': self.make_table(
                    'Tabel XOR Bagian Kiri Round 2',
                    [str(i) for i in range(1, 5)],
                    [
                        ('L setelah SW', self.to_str(sw_left)),
                        (f'F(R,{round2_key_name})', rf2['p4_result']),
                        ('L2', self.to_str(l2)),
                    ],
                    'Tidak ada swap setelah Round 2.'
                ),
            },
            'inverse_ip': {
                'input': combined_str,
                'output': output,
                'table': self.make_table(
                    'Tabel Inverse Initial Permutation',
                    [str(i) for i in range(1, 9)],
                    [
                        ('L2 || R2', combined_str),
                        ('IP⁻¹(L2||R2)', output),
                    ],
                    f'Hasil akhir {"enkripsi" if mode == "encrypt" else "dekripsi"} adalah {output}.'
                ),
            },
            'tables': {
                'P10': self.P10,
                'P8': self.P8,
                'IP': self.IP,
                'IP_INV': self.IP_INV,
                'EP': self.EP,
                'P4': self.P4,
                'S0': self.S0,
                'S1': self.S1,
            }
        }
