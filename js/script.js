// Utility functions
function mod(n, m) {
    return ((n % m) + m) % m;
}

function gcd(a, b) {
    return b === 0 ? a : gcd(b, a % b);
}

function isCoprime(a, b) {
    return gcd(a, b) === 1;
}

function letterToNum(c) {
    return c.toUpperCase().charCodeAt(0) - 65;
}

function numToLetter(n) {
    return String.fromCharCode(mod(n, 26) + 65);
}

function cleanText(text) {
    return text.toUpperCase().replace(/[^A-Z]/g, '');
}

// Caesar Cipher Cryptanalysis
function caesarCryptanalysis(ciphertext) {
    let results = [];
    for (let shift = 0; shift < 26; shift++) {
        let plaintext = '';
        for (let char of ciphertext) {
            if (/[A-Z]/.test(char)) {
                plaintext += numToLetter(letterToNum(char) - shift);
            } else {
                plaintext += char;
            }
        }
        results.push(`Shift ${shift}: ${plaintext}`);
    }
    return results.join('\n');
}

// Affine Cipher Cryptanalysis
function affineCryptanalysis(ciphertext) {
    let results = [];
    for (let a = 1; a < 26; a++) {
        if (!isCoprime(a, 26)) continue;
        for (let b = 0; b < 26; b++) {
            let plaintext = '';
            for (let char of ciphertext) {
                if (/[A-Z]/.test(char)) {
                    let x = letterToNum(char);
                    let invA = modInverse(a, 26);
                    let decrypted = mod(invA * (x - b), 26);
                    plaintext += numToLetter(decrypted);
                } else {
                    plaintext += char;
                }
            }
            results.push(`a=${a}, b=${b}: ${plaintext}`);
        }
    }
    return results.join('\n');
}

function modInverse(a, m) {
    for (let i = 1; i < m; i++) {
        if (mod(a * i, m) === 1) return i;
    }
    return 1;
}

// Vigenere Cipher Cryptanalysis (simplified)
function vigenereCryptanalysis(ciphertext) {
    // For simplicity, assume key length 1-10, use frequency analysis
    let results = [];
    for (let keyLen = 1; keyLen <= 10; keyLen++) {
        let key = '';
        for (let i = 0; i < keyLen; i++) {
            let substr = '';
            for (let j = i; j < ciphertext.length; j += keyLen) {
                substr += ciphertext[j];
            }
            // Simple frequency: assume most common is 'E'
            let freq = {};
            for (let c of substr) {
                if (/[A-Z]/.test(c)) freq[c] = (freq[c] || 0) + 1;
            }
            let mostCommon = Object.keys(freq).reduce((a, b) => freq[a] > freq[b] ? a : b, 'A');
            let shift = mod(letterToNum(mostCommon) - letterToNum('E'), 26);
            key += numToLetter(shift);
        }
        // Decrypt with key
        let plaintext = '';
        let keyIndex = 0;
        for (let char of ciphertext) {
            if (/[A-Z]/.test(char)) {
                let shift = letterToNum(key[keyIndex % keyLen]);
                plaintext += numToLetter(letterToNum(char) - shift);
                keyIndex++;
            } else {
                plaintext += char;
            }
        }
        results.push(`Key length ${keyLen}, Key: ${key}: ${plaintext}`);
    }
    return results.join('\n');
}

// Playfair Cipher Cryptanalysis (basic)
function playfairCryptanalysis(ciphertext) {
    // This is complex; for now, just return a note
    return "Playfair cryptanalysis is complex. Requires digraph frequency analysis and key reconstruction. Not fully implemented yet.";
}

// Hill Cipher Cryptanalysis
function hillCryptanalysis(ciphertext, size) {
    // For small matrices, brute force
    if (size === 2) {
        let results = [];
        for (let a = 0; a < 26; a++) {
            for (let b = 0; b < 26; b++) {
                for (let c = 0; c < 26; c++) {
                    for (let d = 0; d < 26; d++) {
                        let det = mod(a * d - b * c, 26);
                        if (det === 0 || !isCoprime(det, 26)) continue;
                        // Decrypt
                        let invDet = modInverse(det, 26);
                        let invMatrix = [
                            mod(d * invDet, 26), mod(-b * invDet, 26),
                            mod(-c * invDet, 26), mod(a * invDet, 26)
                        ];
                        let plaintext = '';
                        for (let i = 0; i < ciphertext.length; i += 2) {
                            let x1 = letterToNum(ciphertext[i]);
                            let x2 = letterToNum(ciphertext[i+1] || 'X');
                            let y1 = mod(invMatrix[0] * x1 + invMatrix[1] * x2, 26);
                            let y2 = mod(invMatrix[2] * x1 + invMatrix[3] * x2, 26);
                            plaintext += numToLetter(y1) + numToLetter(y2);
                        }
                        results.push(`Matrix [${a},${b};${c},${d}]: ${plaintext}`);
                    }
                }
            }
        }
        return results.slice(0, 10).join('\n'); // Limit output
    }
    return "Hill cipher for size 3 not implemented.";
}

// Keyword Cipher Cryptanalysis
function keywordCryptanalysis(ciphertext) {
    // Assume keyword is common words, but simplified
    let commonKeywords = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'HAD', 'BY', 'WORD', 'HOW', 'SAID', 'EACH', 'WHICH', 'SHE', 'DO', 'AN', 'THEIR', 'TIME', 'IF', 'WILL', 'WAY', 'ABOUT', 'MANY', 'THEN', 'THEM', 'WRITE', 'WOULD', 'LIKE', 'SO', 'THESE', 'HER', 'LONG', 'MAKE', 'THING', 'SEE', 'HIM', 'TWO', 'HAS', 'LOOK', 'MORE', 'DAY', 'COULD', 'GO', 'COME', 'DID', 'NUMBER', 'SOUND', 'NO', 'MOST', 'PEOPLE', 'MY', 'OVER', 'KNOW', 'WATER', 'THAN', 'CALL', 'FIRST', 'WHO', 'MAY', 'DOWN', 'SIDE', 'BEEN', 'NOW', 'FIND'];
    let results = [];
    for (let keyword of commonKeywords.slice(0, 10)) { // Limit
        let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let key = keyword + alphabet.split('').filter(c => !keyword.includes(c)).join('');
        let plaintext = '';
        for (let char of ciphertext) {
            if (/[A-Z]/.test(char)) {
                let index = key.indexOf(char);
                plaintext += alphabet[index];
            } else {
                plaintext += char;
            }
        }
        results.push(`Keyword ${keyword}: ${plaintext}`);
    }
    return results.join('\n');
}

// Columnar Transposition Cryptanalysis
function columnarCryptanalysis(ciphertext, cols) {
    let rows = Math.ceil(ciphertext.length / cols);
    let results = [];
    // Try all permutations of column order
    let indices = Array.from({length: cols}, (_, i) => i);
    let permutations = getPermutations(indices);
    for (let perm of permutations.slice(0, 10)) { // Limit
        let grid = Array.from({length: rows}, () => Array(cols).fill(''));
        let idx = 0;
        for (let c of perm) {
            for (let r = 0; r < rows; r++) {
                if (idx < ciphertext.length) {
                    grid[r][c] = ciphertext[idx++];
                }
            }
        }
        let plaintext = '';
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                plaintext += grid[r][c];
            }
        }
        results.push(`Order ${perm.join('')}: ${plaintext}`);
    }
    return results.join('\n');
}

function getPermutations(arr) {
    if (arr.length <= 1) return [arr];
    let result = [];
    for (let i = 0; i < arr.length; i++) {
        let rest = arr.slice(0, i).concat(arr.slice(i + 1));
        let perms = getPermutations(rest);
        for (let perm of perms) {
            result.push([arr[i], ...perm]);
        }
    }
    return result;
}

// Autokey Cipher Cryptanalysis (similar to Vigenere)
function autokeyCryptanalysis(ciphertext) {
    // Simplified, assume key length 3-5
    let results = [];
    for (let keyLen = 3; keyLen <= 5; keyLen++) {
        // Assume first keyLen chars are key
        let key = ciphertext.slice(0, keyLen);
        let plaintext = key;
        for (let i = 0; i < ciphertext.length; i++) {
            let shift = letterToNum(plaintext[i]);
            let decrypted = numToLetter(letterToNum(ciphertext[i]) - shift);
            plaintext += decrypted;
        }
        plaintext = plaintext.slice(keyLen);
        results.push(`Key length ${keyLen}: ${plaintext}`);
    }
    return results.join('\n');
}

// Running Key Cipher Cryptanalysis
function runningCryptanalysis(ciphertext) {
    return "Running key cipher cryptanalysis requires a known running key text. Not implemented.";
}

// Stream Cipher Cryptanalysis
function streamCryptanalysis(ciphertext) {
    // Assume XOR with repeating key
    let hex = ciphertext.replace(/\s/g, '');
    let bytes = [];
    for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
    }
    // Try short keys
    let results = [];
    for (let keyLen = 1; keyLen <= 5; keyLen++) {
        let key = [];
        for (let i = 0; i < keyLen; i++) {
            key.push(bytes[i] ^ 32); // Assume space
        }
        let plaintext = '';
        for (let i = 0; i < bytes.length; i++) {
            plaintext += String.fromCharCode(bytes[i] ^ key[i % keyLen]);
        }
        results.push(`Key length ${keyLen}: ${plaintext}`);
    }
    return results.join('\n');
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('caesar-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('caesar-input').value);
        let output = caesarCryptanalysis(input);
        document.getElementById('caesar-output').textContent = output;
    });

    document.getElementById('affine-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('affine-input').value);
        let output = affineCryptanalysis(input);
        document.getElementById('affine-output').textContent = output;
    });

    document.getElementById('vigenere-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('vigenere-input').value);
        let output = vigenereCryptanalysis(input);
        document.getElementById('vigenere-output').textContent = output;
    });

    document.getElementById('playfair-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('playfair-input').value);
        let output = playfairCryptanalysis(input);
        document.getElementById('playfair-output').textContent = output;
    });

    document.getElementById('hill-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('hill-input').value);
        let size = parseInt(document.getElementById('hill-keysize').value);
        let output = hillCryptanalysis(input, size);
        document.getElementById('hill-output').textContent = output;
    });

    document.getElementById('keyword-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('keyword-input').value);
        let output = keywordCryptanalysis(input);
        document.getElementById('keyword-output').textContent = output;
    });

    document.getElementById('columnar-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('columnar-input').value);
        let cols = parseInt(document.getElementById('columnar-cols').value);
        let output = columnarCryptanalysis(input, cols);
        document.getElementById('columnar-output').textContent = output;
    });

    document.getElementById('autokey-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('autokey-input').value);
        let output = autokeyCryptanalysis(input);
        document.getElementById('autokey-output').textContent = output;
    });

    document.getElementById('running-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = cleanText(document.getElementById('running-input').value);
        let output = runningCryptanalysis(input);
        document.getElementById('running-output').textContent = output;
    });

    document.getElementById('stream-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let input = document.getElementById('stream-input').value;
        let output = streamCryptanalysis(input);
        document.getElementById('stream-output').textContent = output;
    });
});