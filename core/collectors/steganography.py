import os
import struct
import base64
from PIL import Image
import io

class SteganographyModule:
    def __init__(self):
        self.hidden_data = {}
        
    def hide_data_in_image(self, data, image_path, output_path):
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            data_bytes = data.encode('utf-8')
            data_length = len(data_bytes)
            
            pixels = list(img.getdata())
            
            if data_length * 8 > len(pixels) * 3:
                return False
            
            binary_data = ''.join([format(byte, '08b') for byte in data_bytes])
            binary_length = format(data_length, '032b')
            
            full_binary = binary_length + binary_data
            
            pixel_index = 0
            bit_index = 0
            
            new_pixels = []
            
            for pixel in pixels:
                r, g, b = pixel
                
                if bit_index < len(full_binary):
                    r = (r & 0xFE) | int(full_binary[bit_index])
                    bit_index += 1
                
                if bit_index < len(full_binary):
                    g = (g & 0xFE) | int(full_binary[bit_index])
                    bit_index += 1
                
                if bit_index < len(full_binary):
                    b = (b & 0xFE) | int(full_binary[bit_index])
                    bit_index += 1
                
                new_pixels.append((r, g, b))
            
            new_img = Image.new('RGB', img.size)
            new_img.putdata(new_pixels)
            new_img.save(output_path)
            
            return True
            
        except Exception:
            return False
    
    def extract_data_from_image(self, image_path):
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            
            binary_length = ''
            
            pixel_count = min(11, len(pixels))
            for i in range(pixel_count):
                r, g, b = pixels[i]
                binary_length += str(r & 1)
                binary_length += str(g & 1)
                binary_length += str(b & 1)
            
            if len(binary_length) < 32:
                return None
            
            data_length = int(binary_length[:32], 2)
            
            if data_length <= 0 or data_length > 1000000:
                return None
            
            binary_data = ''
            bit_count = 0
            needed_bits = data_length * 8
            
            for pixel in pixels:
                if bit_count >= 32 + needed_bits:
                    break
                
                r, g, b = pixel
                
                if bit_count >= 32:
                    binary_data += str(r & 1)
                if bit_count + 1 >= 32 and len(binary_data) < needed_bits:
                    binary_data += str(g & 1)
                if bit_count + 2 >= 32 and len(binary_data) < needed_bits:
                    binary_data += str(b & 1)
                
                bit_count += 3
            
            if len(binary_data) < needed_bits:
                return None
            
            binary_data = binary_data[:needed_bits]
            
            data_bytes = []
            for i in range(0, len(binary_data), 8):
                byte_str = binary_data[i:i+8]
                if len(byte_str) == 8:
                    data_bytes.append(int(byte_str, 2))
            
            return bytes(data_bytes).decode('utf-8', errors='ignore')
            
        except Exception:
            return None
    
    def hide_in_ntfs_ads(self, file_path, stream_name, data):
        try:
            if not os.path.exists(file_path):
                return False
            
            ads_path = f"{file_path}:{stream_name}"
            
            with open(ads_path, 'w', encoding='utf-8') as f:
                f.write(data)
            
            return True
            
        except Exception:
            return False
    
    def read_from_ntfs_ads(self, file_path, stream_name):
        try:
            ads_path = f"{file_path}:{stream_name}"
            
            with open(ads_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception:
            return None
    
    def list_ntfs_ads(self, file_path):
        try:
            import subprocess
            
            result = subprocess.run(
                ['dir', '/r', file_path],
                shell=True,
                capture_output=True,
                text=True
            )
            
            streams = []
            for line in result.stdout.split('\n'):
                if ':' in line and '$DATA' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        stream_name = parts[1].split()[0]
                        streams.append(stream_name)
            
            return streams
            
        except Exception:
            return []
    
    def hide_in_registry(self, key_path, value_name, data):
        try:
            import winreg
            
            encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, encoded_data)
            winreg.CloseKey(key)
            
            return True
            
        except Exception:
            return False
    
    def read_from_registry(self, key_path, value_name):
        try:
            import winreg
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            encoded_data, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            
            return base64.b64decode(encoded_data).decode('utf-8')
            
        except Exception:
            return None
    
    def hide_in_slack_space(self, file_path, data):
        try:
            if not os.path.exists(file_path):
                return False
            
            file_size = os.path.getsize(file_path)
            cluster_size = 4096
            
            used_clusters = (file_size + cluster_size - 1) // cluster_size
            slack_space = (used_clusters * cluster_size) - file_size
            
            if len(data) >= slack_space:
                return False
            
            with open(file_path, 'r+b') as f:
                f.seek(file_size)
                f.write(data.encode('utf-8'))
            
            return True
            
        except Exception:
            return False
    
    def read_from_slack_space(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            cluster_size = 4096
            
            used_clusters = (file_size + cluster_size - 1) // cluster_size
            total_allocated = used_clusters * cluster_size
            
            if total_allocated <= file_size:
                return None
            
            with open(file_path, 'rb') as f:
                f.seek(file_size)
                slack_data = f.read(total_allocated - file_size)
            
            return slack_data.decode('utf-8', errors='ignore').strip('\x00')
            
        except Exception:
            return None
    
    def create_polyglot_file(self, image_path, archive_data, output_path):
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
            
            combined_data = img_data + archive_data
            
            with open(output_path, 'wb') as output_file:
                output_file.write(combined_data)
            
            return True
            
        except Exception:
            return False
    
    def extract_from_polyglot(self, polyglot_path):
        try:
            with open(polyglot_path, 'rb') as f:
                data = f.read()
            
            zip_signatures = [b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08']
            rar_signature = b'Rar!\x1a\x07\x00'
            
            for sig in zip_signatures:
                pos = data.find(sig)
                if pos > 0:
                    return data[pos:]
            
            pos = data.find(rar_signature)
            if pos > 0:
                return data[pos:]
            
            return None
            
        except Exception:
            return None
    
    def hide_in_metadata(self, image_path, key, value, output_path):
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            img = Image.open(image_path)
            
            if hasattr(img, '_getexif'):
                exif_dict = img._getexif()
                if exif_dict is None:
                    exif_dict = {}
            else:
                exif_dict = {}
            
            for tag_id, tag_value in exif_dict.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == key:
                    exif_dict[tag_id] = value
                    break
            else:
                comment_tag = 270
                exif_dict[comment_tag] = f"{key}:{value}"
            
            img.save(output_path, exif=exif_dict)
            return True
            
        except Exception:
            return False
    
    def read_metadata(self, image_path, key=None):
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            img = Image.open(image_path)
            
            if hasattr(img, '_getexif'):
                exif_dict = img._getexif()
            else:
                return None
            
            if exif_dict is None:
                return None
            
            metadata = {}
            for tag_id, tag_value in exif_dict.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata[tag_name] = tag_value
            
            if key:
                return metadata.get(key)
            
            return metadata
            
        except Exception:
            return None
    
    def hide_in_whitespace(self, text_file, hidden_text, output_file):
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            binary_hidden = ''.join([format(ord(char), '08b') for char in hidden_text])
            
            lines = content.split('\n')
            modified_lines = []
            
            bit_index = 0
            for line in lines:
                if bit_index < len(binary_hidden):
                    if binary_hidden[bit_index] == '1':
                        line = line + ' '
                    bit_index += 1
                modified_lines.append(line)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(modified_lines))
            
            return True
            
        except Exception:
            return False
    
    def extract_from_whitespace(self, text_file):
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            binary_data = ''
            
            for line in lines:
                if line.endswith(' '):
                    binary_data += '1'
                else:
                    binary_data += '0'
            
            if len(binary_data) % 8 != 0:
                binary_data = binary_data[:-(len(binary_data) % 8)]
            
            hidden_text = ''
            for i in range(0, len(binary_data), 8):
                byte_str = binary_data[i:i+8]
                if len(byte_str) == 8:
                    char_code = int(byte_str, 2)
                    if 32 <= char_code <= 126:
                        hidden_text += chr(char_code)
            
            return hidden_text
            
        except Exception:
            return None
