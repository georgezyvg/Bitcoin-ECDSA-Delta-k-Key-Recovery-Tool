from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import generator_secp256k1
from tqdm import trange

def modinv(a, n):
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"Odwrotność modulo nie istnieje dla {a} mod {n}")
    if t < 0:
        t += n
    return t

def compute_private_key(z1, z2, r1, r2, s1, s2, delta_k, n):
    numerator = (delta_k * s1 * s2 - (s2 * z1 - s1 * z2)) % n
    denominator = (s2 * r1 - s1 * r2) % n
    inv_denominator = modinv(denominator, n)
    d = (numerator * inv_denominator) % n
    return d

def compute_ephemeral_key(z, r, s, d, n):
    inv_s = modinv(s, n)
    k = (z + d * r) * inv_s % n
    return k

def get_compressed_pubkey(d):
    G = generator_secp256k1
    pub_point = d * G
    prefix = b'\x02' if pub_point.y() % 2 == 0 else b'\x03'
    compressed = prefix + pub_point.x().to_bytes(32, 'big')
    return compressed.hex()

def main():
    # 🔢 Wstawione dane z podpisów
    z1 = int("0cf7190cc6c1f95b987e0e284e4eba44552f89662272b850b059a8dc0d8905a8  ", 16)
    z2 = int("c7c58a952ca7b31ced67bfea57fd7571314f8d77a88c90f42e68bdd82c2adb4f", 16)
    r1 = int("ab9467e44699c0ab5ee2da6389e1646725a03bd66433eb99e531e45d76476ee0", 16)
    r2 = int("a674f3ced3e25621cde299d20a700ccab080eb8352db313c5e039473ae48df83", 16)
    s1 = int("59098b9fe30776049508f91eea10e4a9972eec2c1afe79674379578447b7aa46", 16)
    s2 = int("57d8156cb1f7d1b390a13bc008bb3f2478d5552d00cc75215f21bbef866bec55", 16)

    # 🧠 Oczekiwany publiczny klucz – podmień na właściwy
    expected_pubkey = "02174ee672429ff94304321cdae1fc1e487edf658b34bd1d36da03761658a2bb09"

    # secp256k1 curve order
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    print("🔍 Szukam poprawnej różnicy delta_k...\n")

    for delta_k in trange(1, 1000000):  # 🔁 Możesz zwiększyć zakres
        try:
            d = compute_private_key(z1, z2, r1, r2, s1, s2, delta_k, n)
            k1 = compute_ephemeral_key(z1, r1, s1, d, n)
            k2 = compute_ephemeral_key(z2, r2, s2, d, n)

            if (k1 - k2) % n == delta_k:
                pubkey = get_compressed_pubkey(d)

                print(f"\n🔥 Znaleziono potencjalne delta_k = {delta_k}")
                print(f"🔑 Prywatny klucz d = {hex(d)}")
                print(f"🔐 Publiczny klucz (skompresowany) = {pubkey}")
                print(f"k1 = {k1}")
                print(f"k2 = {k2}")
                print(f"Różnica (k1 - k2) = {(k1 - k2) % n}")

                if pubkey.lower() == expected_pubkey.lower():
                    print("✅ Publiczny klucz się ZGADZA!")
                    break
                else:
                    print("❌ Publiczny klucz NIE pasuje – szukam dalej...\n")
        except ValueError:
            continue

    print("🔚 Szukanie zakończone.")

if __name__ == '__main__':
    main()
