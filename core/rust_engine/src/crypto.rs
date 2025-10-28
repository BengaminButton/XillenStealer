use chacha20poly1305::{ChaCha20Poly1305, Key, Nonce, aead::{Aead, KeyInit}};
use aes_gcm::{Aes256Gcm, aead::generic_array::GenericArray};
use blake3::Hasher;
use rand::Rng;
use std::collections::HashMap;

pub struct CryptoEngine {
    keys: HashMap<String, Vec<u8>>,
}

impl CryptoEngine {
    pub fn new() -> Self {
        CryptoEngine {
            keys: HashMap::new(),
        }
    }

    pub fn encrypt_chacha20(&self, data: &str, key_id: Option<&str>) -> String {
        let key = match key_id {
            Some(id) => self.get_or_generate_key(id),
            None => self.generate_random_key(),
        };

        let cipher = ChaCha20Poly1305::new(&Key::from_slice(&key));
        let nonce_bytes: [u8; 12] = rand::thread_rng().gen();
        let nonce = Nonce::from_slice(&nonce_bytes);

        match cipher.encrypt(nonce, data.as_bytes()) {
            Ok(ciphertext) => {
                let mut result = nonce_bytes.to_vec();
                result.extend_from_slice(&ciphertext);
                base64::encode(result)
            }
            Err(_) => String::new(),
        }
    }

    pub fn decrypt_chacha20(&self, encrypted: &str, key_id: Option<&str>) -> String {
        let key = match key_id {
            Some(id) => match self.keys.get(id) {
                Some(k) => k.clone(),
                None => return String::new(),
            },
            None => return String::new(),
        };

        let data = match base64::decode(encrypted) {
            Ok(d) => d,
            Err(_) => return String::new(),
        };

        if data.len() < 12 {
            return String::new();
        }

        let (nonce_bytes, ciphertext) = data.split_at(12);
        let cipher = ChaCha20Poly1305::new(&Key::from_slice(&key));
        let nonce = Nonce::from_slice(nonce_bytes);

        match cipher.decrypt(nonce, ciphertext) {
            Ok(plaintext) => String::from_utf8_lossy(&plaintext).to_string(),
            Err(_) => String::new(),
        }
    }

    pub fn encrypt_aes256(&self, data: &str, key: &[u8]) -> String {
        if key.len() != 32 {
            return String::new();
        }

        let cipher = Aes256Gcm::new(GenericArray::from_slice(key));
        let nonce_bytes: [u8; 12] = rand::thread_rng().gen();
        let nonce = GenericArray::from_slice(&nonce_bytes);

        match cipher.encrypt(nonce, data.as_bytes()) {
            Ok(ciphertext) => {
                let mut result = nonce_bytes.to_vec();
                result.extend_from_slice(&ciphertext);
                base64::encode(result)
            }
            Err(_) => String::new(),
        }
    }

    pub fn hash_blake3(&self, data: &str) -> String {
        let mut hasher = Hasher::new();
        hasher.update(data.as_bytes());
        let hash = hasher.finalize();
        hex::encode(hash.as_bytes())
    }

    pub fn derive_key(&self, password: &str, salt: &[u8]) -> Vec<u8> {
        let mut hasher = Hasher::new();
        hasher.update(password.as_bytes());
        hasher.update(salt);
        hasher.finalize().as_bytes()[..32].to_vec()
    }

    fn get_or_generate_key(&self, key_id: &str) -> Vec<u8> {
        match self.keys.get(key_id) {
            Some(key) => key.clone(),
            None => self.generate_random_key(),
        }
    }

    fn generate_random_key(&self) -> Vec<u8> {
        let mut key = vec![0u8; 32];
        rand::thread_rng().fill(&mut key[..]);
        key
    }

    pub fn hardware_rng(&self) -> Option<u64> {
        unsafe {
            let mut result: u64 = 0;
            if std::arch::x86_64::_rdrand64_step(&mut result) == 1 {
                Some(result)
            } else {
                None
            }
        }
    }

    pub fn cpu_features(&self) -> HashMap<String, bool> {
        let mut features = HashMap::new();
        
        if std::arch::is_x86_feature_detected!("aes") {
            features.insert("aes".to_string(), true);
        }
        if std::arch::is_x86_feature_detected!("avx2") {
            features.insert("avx2".to_string(), true);
        }
        if std::arch::is_x86_feature_detected!("rdrand") {
            features.insert("rdrand".to_string(), true);
        }
        
        features
    }
}
