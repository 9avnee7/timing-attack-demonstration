import time
import string
import hmac


# --- Weak (vulnerable) comparison function ---
def weak_compare(input_str, secret_str):
    if len(input_str) != len(secret_str):
        return False
    for i in range(len(secret_str)):
        if input_str[i] != secret_str[i]:
            return False
        time.sleep(0.0001)  # Artificial delay per matched character
    time.sleep(0.001)  # Final delay after full match
    return True

# --- Secure constant-time comparison function ---
def secure_compare(input_str, secret_str):
    return hmac.compare_digest(input_str, secret_str)

# --- Timing measurement function ---
def measure_time(guess, secret, trials=20, use_secure=False):
    total = 0
    for _ in range(trials):
        start = time.perf_counter_ns()
        if use_secure:
            secure_compare(guess, secret)
        else:
            weak_compare(guess, secret)
        end = time.perf_counter_ns()
        total += end - start
    return total / trials

# --- Timing attack logic for weak comparison only ---
def run_timing_attack(secret, use_secure=False):
    if use_secure:
        print("\n[!] Secure comparison enabled. Timing attack should fail.\n")

    CHARSET = string.ascii_letters + string.digits
    PLACEHOLDER = "_"
    secret_length = len(secret)
    best_guess = [PLACEHOLDER] * secret_length
        # Initialize a dictionary to store timing results
    timing_results = {
        pos: {char: [] for char in CHARSET}
        for pos in range(secret_length)
    }

    for pos in range(secret_length):
        print(f"\n[+] Guessing character at position {pos}")
        
        # Try every character in the charset
        for char in CHARSET:
            guess = (
                ''.join(best_guess[:pos]) +  # Known guesses
                char +                        # Current guess
                PLACEHOLDER * (secret_length - pos - 1)  # Fillers
            )

            # Measure average time
            avg_time = measure_time(guess, secret, trials=500,use_secure=use_secure)

            # Store timing result
            timing_results[pos][char].append(avg_time)

            # print(f"    Tried '{char}' at pos {pos} → Avg time: {avg_time:.2f} ns")

        # Find character with max average timing
        avg_char_times = {
            c: sum(times)/len(times)
            for c, times in timing_results[pos].items()
        }

        best_char = max(avg_char_times, key=avg_char_times.get)
        best_guess[pos] = best_char

        print(f"[✓] Best guess at position {pos}: '{best_char}' with avg time {avg_char_times[best_char]:.2f} ns")

    # Final guess after full loop
    final_guess = ''.join(best_guess)
    print(f"\n[*] Final inferred secret: {final_guess}")

    # Optional: Compare to actual secret
    print("[✓] Correct!" if final_guess == secret else "[✗] Incorrect")



# --- Main execution ---
if __name__ == "__main__":
    SECRET = "s3cr3tnavneet"

    print("\n--- Phase 1: Timing Attack on Weak Comparison ---")
    run_timing_attack(SECRET, use_secure=False)

    print("\n--- Phase 2: Secure Comparison Demonstration ---")
    print("[*] Running same attack using secure_compare (should fail to extract secret)...")
    run_timing_attack(SECRET, use_secure=True)

    print("\n--- Benchmark: Timing Difference Demo ---")
    sample_guess = "s3cr3tnavneat"  

    weak_time = measure_time(sample_guess, SECRET, trials=1000, use_secure=False)
    secure_time = measure_time(sample_guess, SECRET, trials=1000, use_secure=True)

    print(f"[*] Avg time (weak_compare):   {weak_time:.2f} ns")
    print(f"[*] Avg time (secure_compare): {secure_time:.2f} ns")
    
