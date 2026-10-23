"""otp: libreta de un solo uso (Shannon 1949, doi:10.1002/j.1538-7305.1949.tb00928.x), el único cifrado con seguridad
incondicional demostrada, y solo si la clave es aleatoria, tan larga como el mensaje, secreta y no se reutiliza nunca.
La distribución de la clave es el problema real (p. ej. QKD); para uso práctico se recomienda ML-KEM (NIST FIPS 203).
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import secrets


def keygen(n):
    return secrets.token_bytes(n)


def xor(data: bytes, key: bytes) -> bytes:
    if len(key) < len(data):
        raise ValueError("la clave debe ser al menos tan larga como el mensaje")
    return bytes(a ^ b for a, b in zip(data, key))


encrypt = decrypt = xor
