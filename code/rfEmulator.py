import binascii

class RFEmulator:
    """A class to emulate RF encoding and decoding over Twitch chat."""

    def encode_hex(self, hex_str):
        """Encodes a hex string into a Manchester-modulated Base64 string."""
        try:
            bin_str = ''.join(format(int(c, 16), '04b') for c in hex_str)
        except ValueError:
            raise ValueError("Invalid hex character encountered during encoding.")

        man_str = ''.join("10" if c == "1" else "01" for c in bin_str)

        byte_data = int(man_str, 2).to_bytes((len(man_str) + 7) // 8, byteorder='big')

        return binascii.b2a_base64(byte_data).decode('latin1').strip()

    def decode_man_base(self, base_str):
        """Decodes a Manchester-modulated Base64 string back into hex."""
        try:
            temp_hex = binascii.b2a_hex(binascii.a2b_base64(base_str)).decode()
        except binascii.Error:
            raise ValueError("Invalid Base64 input during decoding.")

        man_str = ''.join(format(int(c, 16), '04b') for c in temp_hex)

        bin_str = ''.join("1" if man_str[i:i+2] == "10" else "0" for i in range(0, len(man_str), 2))

        hex_str = format(int(bin_str, 2), 'x')

        return hex_str
