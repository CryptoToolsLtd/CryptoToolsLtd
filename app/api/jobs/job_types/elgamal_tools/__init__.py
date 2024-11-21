from crypto import is_prime, fact, pad, unpad, BitPaddingConfig, is_primitive_root_fast # type: ignore
from ..cert import issue_computation_cert, verify_computation_cert
import json

def elgamal_check_p_certificate(p: int, p_certificate: str):
    if p < 1:
        raise ValueError("Invalid number of bits for p")
    if p.bit_length() > 8192:
        raise ValueError("Number of bits for p is too large")
    
    if not is_prime(p):
        raise ValueError("p is not a prime number")
    
    rely_on_certificate = False
    fact_of_p_minus_1: dict[int, int] = {}
    if p_certificate:
        try:
            print("Checking cert")
            payload = verify_computation_cert("ElGamalGeneratePAlphaA", p_certificate)
            print("OK, checking payload p")
            p_in_certificate = int(payload["p"])
            print("OK, checking payload fact_of_p_minus_1")
            fact_of_p_minus_1_loaded = json.loads(payload["fact_of_p_minus_1"])
            print(f"OK, checking factors: {fact_of_p_minus_1_loaded}")

            prod = 1
            for f in fact_of_p_minus_1_loaded:
                base = int(f)
                if not is_prime(base):
                    raise ValueError("Non-prime factor in fact_of_p_minus_1")
                exponent = fact_of_p_minus_1_loaded[f]
                if not isinstance(exponent, int) or exponent < 1: # type: ignore
                    raise ValueError("Invalid factor in fact_of_p_minus_1")
                prod *= base ** exponent
                fact_of_p_minus_1[base] = exponent

            print("OK, checking product")
            if (
                p_in_certificate == p
                and p - 1 == prod
            ):
                rely_on_certificate = True
            print("Everything is OK")
        except Exception as e:
            print("Error in certificate")
            print(f"{e.__class__.__name__}: {e}")
    
    if not rely_on_certificate:
        fact_of_p_minus_1 = fact(p - 1)
        p_certificate = issue_computation_cert("ElGamalGeneratePAlphaA", {
            "p": str(p),
            "fact_of_p_minus_1": json.dumps(fact_of_p_minus_1),
        })
        print(f"Generated certificate for fact_of_p_minus_1: {fact_of_p_minus_1}\n")
    else:
        print(f"Relying on certificate for fact_of_p_minus_1: {fact_of_p_minus_1}\n")
    
    return fact_of_p_minus_1

def convert_plain_number_to_primitive_root(BIT_PADDING_CONFIG: BitPaddingConfig, p: int, original_number: int, fact_of_p_minus_1: dict[int, int]) -> int:
    def check_func(candidate: int) -> bool:
        return is_primitive_root_fast(p, candidate, fact_of_p_minus_1)
    padded_number = pad(BIT_PADDING_CONFIG, original_number, check_func)
    if padded_number is None:
        raise RuntimeError(f"Could not find a valid primitive root x modulo p = {p} substituting original_number m = {original_number}. Consider increasing padding, increasing p, or changing the message m.")
    return padded_number

def convert_primitive_root_to_plain_number(BIT_PADDING_CONFIG: BitPaddingConfig, primitive_root: int) -> int:
    return unpad(BIT_PADDING_CONFIG, primitive_root)
