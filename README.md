# 🔢 Bitcoin ECDSA Delta-k Key Recovery Tool

> ⚠️ **Research & Educational Use Only**  
> This project demonstrates an advanced **ECDSA delta-k recovery technique**.  
> It is **not** intended for unauthorized private key recovery or exploitation.  
> Use only on data you own or for which you have **explicit permission** to test.

---

## 🚀 Overview

This Python script attempts to recover an **ECDSA private key** when two signatures use **ephemeral nonces (`k1`, `k2`)** that differ by a **known or small integer delta (`Δk`)**.  

It systematically tests a range of possible `Δk` values, computes the corresponding private key `d`, reconstructs ephemeral keys, and verifies correctness by checking the derived **compressed public key**.

---

## ✨ Features

| Feature | Description |
|----------|--------------|
| 🔁 **Brute-force Δk search** | Iterates through possible nonce differences (`k1 - k2 = Δk`) |
| 🧮 **Full ECDSA math** | Implements modular inverse and key equations manually |
| 🔐 **Private & public key reconstruction** | Computes both `d` and compressed public key |
| ⚡ **Fast progress bar** | Uses `tqdm` for visual progress display |
| 🧠 **Deterministic verification** | Verifies by comparing with known public key |
| 📚 **No external blockchain access** | Works purely on local signature data |

---

## 📂 File Structure

| File | Description |
|------|-------------|
| `delta_k_recovery.py` | Main script (the code below) |
| `README.md` | Documentation (this file) |

---

## ⚙️ Configuration

| Variable | Description |
|-----------|-------------|
| `z1`, `z2` | Message hashes from two ECDSA signatures |
| `r1`, `r2` | Signature component `r` values |
| `s1`, `s2` | Signature component `s` values |
| `expected_pubkey` | The expected compressed public key (for verification) |
| `n` | Order of secp256k1 (0xFFFFFFFF...4141) |
| `delta_k` range | Adjustable search range (default: 1 → 1,000,000) |

**Dependencies**
```bash
pip install ecdsa tqdm
🧠 How It Works
1️⃣ ECDSA background

For a given signature (r, s) over message hash z:

s = k⁻¹ (z + r·d) mod n


If two signatures reuse nonces with a fixed difference Δk = k1 − k2,
we can solve for d using modular arithmetic.

2️⃣ Private key recovery formula

The implemented recovery formula:

numerator   = (Δk * s1 * s2 - (s2*z1 - s1*z2)) mod n
denominator = (s2*r1 - s1*r2) mod n
d = numerator * denominator⁻¹ mod n


This yields a candidate private key d for each tested Δk.

3️⃣ Ephemeral key reconstruction

Once a candidate private key is found,
ephemeral nonces are recalculated to confirm correctness:

k = (z + d * r) * s⁻¹ mod n


If (k1 − k2) mod n == Δk,
then Δk is valid and the private key candidate is consistent.

4️⃣ Public key verification

The public key is reconstructed from d:

pubkey = d * G


and compressed as:

02 + x (if y even)
03 + x (if y odd)


If this compressed key matches the expected_pubkey,
the script halts and reports success ✅.

🧾 Example Output
🔍 Szukam poprawnej różnicy delta_k...

🔥 Znaleziono potencjalne delta_k = 74219
🔑 Prywatny klucz d = 0x3ae52e9c2a15b9c76a4e6f75b7d...
🔐 Publiczny klucz (skompresowany) = 02174ee672429ff94304321cdae1fc1e487edf658b34bd1d36da03761658a2bb09
k1 = 548912467...
k2 = 548838248...
Różnica (k1 - k2) = 74219
✅ Publiczny klucz się ZGADZA!

🔚 Szukanie zakończone.

🧩 Core Functions
Function	Purpose
modinv(a, n)	Calculates modular inverse using extended Euclidean algorithm
compute_private_key(...)	Computes candidate private key given two signatures and Δk
compute_ephemeral_key(...)	Derives nonce k from known (r, s, z, d)
get_compressed_pubkey(d)	Derives compressed public key from private key
main()	Performs brute-force search for correct Δk
⚡ Performance Tips

Adjust trange(1, 1_000_000) to expand or narrow your search range.

Disable or batch console logging if testing larger ranges.

The algorithm is pure-Python — for large search spaces, consider parallel execution.

🔒 Ethical & Legal Notice

This repository demonstrates cryptographic key-recovery math for educational research.
It must not be used to obtain or guess private keys of real users or wallets.

You may:

Use it on testnet data or synthetic ECDSA pairs.

Analyze its math for academic learning.

Use it for authorized penetration testing in controlled labs.

You must not:

Run it on blockchain data or any external address without permission.

Distribute modified versions for unauthorized exploitation.

Unauthorized use is illegal and unethical.

🧰 Possible Extensions

🧮 Add automatic range scaling based on r correlation.

💾 Save successful candidates to a JSON or CSV log.

🧠 Integrate a lightweight ML model to guide delta search direction.

⚙️ Add CLI parameters (--start, --end, --pubkey).

🚀 Implement multiprocessing to split search range across CPU cores.

🪪 License

MIT License
© 2025 — Author: [Your Name or Alias]
Free for research, learning, and authorized security testing.

💡 Summary

This project implements a compact and readable ECDSA delta-k attack demonstration that shows:

how nonce reuse or correlation leaks private keys,

how to verify key consistency mathematically, and

how to apply modular arithmetic safely and transparently.

🧠 Learn, don’t exploit — understand cryptography responsibly.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
