import itertools

def is_stable_matching(matching, men_prefs, women_prefs):
    """Check if the given matching is stable."""
    n = len(men_prefs)
    women_partners = {w: m for m, w in matching.items()}

    for m in range(n):
        w = matching[m]
        m_pref = men_prefs[m]
        w_index = m_pref.index(w)
        preferred_women = m_pref[:w_index]

        for w_prime in preferred_women:
            current_m = women_partners.get(w_prime)
            if current_m is None:
                continue
            w_pref = women_prefs[w_prime]
            if w_pref.index(m) < w_pref.index(current_m):
                return False
    return True

def count_stable_matchings(men_prefs, women_prefs):
    """Count all stable matchings given preference lists as index-based lists."""
    n = len(men_prefs)
    stable_count = 0

    for perm in itertools.permutations(range(n)):
        matching = {m: perm[m] for m in range(n)}
        if is_stable_matching(matching, men_prefs, women_prefs):
            stable_count += 1

    return stable_count

# Example usage for n = 4
men_prefs = [[3, 0, 4, 2, 1], [0, 1, 4, 3, 2], [2, 0, 4, 3, 1], [4, 2, 1, 0, 3], [3, 1, 2, 0, 4]]

women_prefs =  [[3, 2, 0, 4, 1], [4, 0, 2, 3, 1], [0, 1, 2, 3, 4], [2, 4, 1, 3, 0], [1, 4, 3, 0, 2]]

import random

def generate_random_preferences(n, seed=None):
    if seed is not None:
        random.seed(seed)
    men_prefs = [random.sample(range(n), n) for _ in range(n)]
    women_prefs = [random.sample(range(n), n) for _ in range(n)]
    return men_prefs, women_prefs

# Try generating random instances and count stable matchings until we find one with > 10
found = False
attempts = 0
max_attempts = 100000
result = None

while not found and attempts < max_attempts:
    men_prefs, women_prefs = generate_random_preferences(5)
    count = count_stable_matchings(men_prefs, women_prefs)
    if count > 7:
        found = True
        result = (count, men_prefs, women_prefs)
    attempts += 1

print(result)


# Men prefer: w1 ≻ w2 ≻ w3 ≻ w4, w2 ≻ w3 ≻ w4 ≻ w1, ...
men_prefs = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 0],
    [2, 3, 0, 4, 1],  # m2 deviates slightly: w0 before w4
    [3, 4, 0, 1, 2],
    [4, 0, 1, 2, 3],
]

women_prefs = [
    [3, 2, 1, 0, 4],
    [0, 4, 1, 3, 2],
    [2, 3, 0, 1, 4],
    [4, 1, 2, 0, 3],
    [1, 0, 3, 4, 2],
]







print(count_stable_matchings(men_prefs, women_prefs))
