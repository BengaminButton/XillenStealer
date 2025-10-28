import random
import base64

class PolymorphicEngine:
    def __init__(self):
        self.instruction_substitutions = self._init_substitutions()
        
    def _init_substitutions(self):
        substitutions = {
            'mov': ['lea', 'push', 'pop'],
            'cmp': ['test', 'and'],
            'jz': ['jne', 'je', 'jmp'],
            'call': ['jmp', 'push'],
        }
        return substitutions
        
    def mutate_code(self, code):
        if isinstance(code, str):
            code = code.encode()
            
        mutated = bytearray(code)
        
        for i in range(len(mutated) - 1):
            if random.random() < 0.1:
                if mutated[i] == 0x48 and mutated[i+1] == 0x8B:
                    mutated[i] = 0x4C
                elif mutated[i] == 0x48 and mutated[i+1] == 0x31:
                    mutated[i] = 0x4D
                    
        return bytes(mutated)
        
    def obfuscate_control_flow(self, code):
        if isinstance(code, str):
            code = code.encode()
            
        obfuscated = bytearray(code)
        
        for i in range(len(obfuscated) - 1):
            if obfuscated[i] == 0x74:
                if random.random() < 0.5:
                    obfuscated[i] = 0x0F
                    obfuscated.insert(i+1, 0x84)
                    obfuscated.insert(i+2, 0x00)
                    obfuscated.insert(i+3, 0x00)
                    obfuscated.insert(i+4, 0x00)
                    obfuscated.insert(i+5, 0x00)
                    
        return bytes(obfuscated)
        
    def inject_dead_code(self, code):
        dead_code_patterns = [
            b'\x90',
            b'\x48\x31\xDB\x48\x31\xDB',
            b'\x90\x90\x90',
        ]
        
        if isinstance(code, str):
            code = code.encode()
            
        modified = bytearray(code)
        
        for i in range(len(modified) - 1):
            if random.random() < 0.05:
                dead_code = random.choice(dead_code_patterns)
                for byte in dead_code:
                    modified.insert(i, byte)
                    i += 1
                    
        return bytes(modified)
        
    def encrypt_strings(self, data):
        if isinstance(data, str):
            data = data.encode()
            
        key = random.randint(1, 255)
        encrypted = bytearray([key])
        
        for byte in data:
            encrypted.append(byte ^ key)
            
        return bytes(encrypted)
        
    def decrypt_strings(self, encrypted):
        if len(encrypted) == 0:
            return b''
            
        key = encrypted[0]
        decrypted = bytearray()
        
        for byte in encrypted[1:]:
            decrypted.append(byte ^ key)
            
        return bytes(decrypted)
        
    def pack_pe(self, pe_data):
        packed = bytearray()
        
        stub = b'\x48\x83\xEC\x28\x48\x8D\x0D\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x48\x83\xC4\x28\xC3'
        packed.extend(stub)
        packed.extend(pe_data)
        
        return bytes(packed)
