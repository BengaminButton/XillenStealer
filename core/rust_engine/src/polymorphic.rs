use rand::Rng;
use std::collections::HashMap;

pub struct PolymorphicEngine {
    instruction_substitutions: HashMap<Vec<u8>, Vec<Vec<u8>>>,
    control_flow_patterns: Vec<ControlFlowPattern>,
}

struct ControlFlowPattern {
    pattern: Vec<u8>,
    obfuscations: Vec<Vec<u8>>,
}

impl PolymorphicEngine {
    pub fn new() -> Self {
        let mut engine = PolymorphicEngine {
            instruction_substitutions: HashMap::new(),
            control_flow_patterns: Vec::new(),
        };
        engine.init_substitutions();
        engine.init_control_flow();
        engine
    }

    fn init_substitutions(&mut self) {
        self.instruction_substitutions.insert(
            vec![0x48, 0x8B, 0xC1],
            vec![
                vec![0x48, 0x89, 0xC8],
                vec![0x4C, 0x8B, 0xC1, 0x49, 0x89, 0xC0],
            ],
        );

        self.instruction_substitutions.insert(
            vec![0x48, 0x31, 0xC0],
            vec![
                vec![0x4D, 0x31, 0xC0, 0x49, 0x89, 0xC0],
                vec![0x48, 0xC7, 0xC0, 0x00, 0x00, 0x00, 0x00],
            ],
        );

        self.instruction_substitutions.insert(
            vec![0x48, 0x83, 0xEC, 0x20],
            vec![
                vec![0x48, 0x81, 0xEC, 0x00, 0x20, 0x00, 0x00],
                vec![0x4C, 0x89, 0xE5, 0x48, 0x83, 0xE4, 0xF0],
            ],
        );
    }

    fn init_control_flow(&mut self) {
        let pattern = vec![0x48, 0x85, 0xC0, 0x74, 0x0A];
        let obfuscations = vec![
            vec![
                0x48, 0x85, 0xC0,
                0x0F, 0x84, 0x00, 0x00, 0x00, 0x00,
                0x90,
            ],
            vec![
                0x48, 0x85, 0xC0,
                0x75, 0x05,
                0xEB, 0x0A,
                0x90, 0x90,
            ],
        ];
        
        self.control_flow_patterns.push(ControlFlowPattern {
            pattern,
            obfuscations,
        });
    }

    pub fn mutate_code(&self, original: &[u8]) -> Vec<u8> {
        let mut result = Vec::new();
        let mut i = 0;
        let mut rng = rand::thread_rng();

        while i < original.len() {
            let mut matched = false;

            for (pattern, alternatives) in &self.instruction_substitutions {
                if i + pattern.len() <= original.len() {
                    if &original[i..i + pattern.len()] == pattern.as_slice() {
                        let alternative = &alternatives[rng.gen_range(0..alternatives.len())];
                        result.extend_from_slice(alternative);
                        i += pattern.len();
                        matched = true;
                        break;
                    }
                }
            }

            if !matched {
                result.push(original[i]);
                i += 1;
            }
        }

        self.obfuscate_control_flow(&mut result)
    }

    fn obfuscate_control_flow(&self, code: &mut Vec<u8>) -> Vec<u8> {
        let mut result = Vec::new();
        let mut i = 0;
        let mut rng = rand::thread_rng();

        while i < code.len() {
            let mut matched = false;

            for pattern_obj in &self.control_flow_patterns {
                let pattern = &pattern_obj.pattern;
                if i + pattern.len() <= code.len() {
                    if &code[i..i + pattern.len()] == pattern.as_slice() {
                        let obfuscation = &pattern_obj.obfuscations[rng.gen_range(0..pattern_obj.obfuscations.len())];
                        result.extend_from_slice(obfuscation);
                        i += pattern.len();
                        matched = true;
                        break;
                    }
                }
            }

            if !matched {
                result.push(code[i]);
                i += 1;
            }
        }

        self.inject_dead_code(result)
    }

    fn inject_dead_code(&self, code: Vec<u8>) -> Vec<u8> {
        let mut result = Vec::new();
        let mut i = 0;
        let mut rng = rand::thread_rng();

        while i < code.len() {
            if rng.gen_bool(0.1) {
                let dead_codes = vec![
                    vec![0x90],
                    vec![0x48, 0x31, 0xDB, 0x48, 0x31, 0xDB],
                    vec![0x90, 0x90, 0x90],
                ];
                let dead_code = &dead_codes[rng.gen_range(0..dead_codes.len())];
                result.extend_from_slice(dead_code);
            }
            result.push(code[i]);
            i += 1;
        }

        result
    }

    pub fn shuffle_registers(&self, code: &[u8]) -> Vec<u8> {
        code.to_vec()
    }

    pub fn encrypt_strings(&self, data: &[u8]) -> Vec<u8> {
        let mut rng = rand::thread_rng();
        let key: u8 = rng.gen();
        let mut encrypted = vec![key];

        for byte in data {
            encrypted.push(byte ^ key);
        }

        encrypted
    }

    pub fn decrypt_strings(&self, encrypted: &[u8]) -> Vec<u8> {
        if encrypted.is_empty() {
            return Vec::new();
        }

        let key = encrypted[0];
        encrypted[1..].iter().map(|&b| b ^ key).collect()
    }

    pub fn pack_pe(&self, pe_data: &[u8]) -> Vec<u8> {
        let compressed = self.compress(pe_data);
        let stub = self.generate_unpacker_stub();
        
        let mut packed = stub;
        packed.extend_from_slice(&compressed);
        packed
    }

    fn compress(&self, data: &[u8]) -> Vec<u8> {
        data.to_vec()
    }

    fn generate_unpacker_stub(&self) -> Vec<u8> {
        vec![
            0x48, 0x83, 0xEC, 0x28,
            0x48, 0x8D, 0x0D, 0x00, 0x00, 0x00, 0x00,
            0xE8, 0x00, 0x00, 0x00, 0x00,
            0x48, 0x83, 0xC4, 0x28,
            0xC3,
        ]
    }
}
