import itertools

def is_stable(matching, men_prefs, women_prefs):
    """Check if the current matching is stable."""
    n = len(men_prefs)
    women_partners = {w: m for m, w in matching.items()}

    for m in range(n):
        w = matching[m]
        m_pref = men_prefs[m]
        w_index = m_pref.index(w)
        for w_pref in m_pref[:w_index]:
            m_prime = women_partners.get(w_pref)
            if m_prime is not None and women_prefs[w_pref].index(m) < women_prefs[w_pref].index(m_prime):
                return False
    return True

def resolve_rom_blocking(matching, arrived, men_prefs, women_prefs):
    """Resolve blocking pairs via best-response updates until stable among arrived agents."""
    n = len(men_prefs)
    updated = True
    max_steps = n * n  # safe upper bound on steps

    for _ in range(max_steps):
        updated = False
        for m in range(n):
            if ('m', m) not in arrived:
                continue
            for w in men_prefs[m]:
                if ('w', w) not in arrived:
                    continue
                m_curr = {v: k for k, v in matching.items()}.get(w)
                m_prefers = m not in matching or men_prefs[m].index(w) < men_prefs[m].index(matching[m])
                w_prefers = m_curr is None or women_prefs[w].index(m) < women_prefs[w].index(m_curr)
                if m_prefers and w_prefers:
                    if m_curr is not None:
                        del matching[m_curr]
                    matching[m] = w
                    updated = True
                    break  # move to next m after successful match
        if not updated:
            break
    return matching


def count_rom_reachable_matchings_full_rom(men_prefs, women_prefs):
    """Full ROM: consider all 2n! arrival orders (men + women), resolve blocking pairs."""
    n = len(men_prefs)
    agents = [('m', i) for i in range(n)] + [('w', i) for i in range(n)]
    reachable_matchings = set()
    count=0
    for perm in itertools.permutations(agents):
        count+=1
        if count%10000==0:
            print(count)
        arrived = set()
        matching = {}
        for agent in perm:
            arrived.add(agent)
            matching = resolve_rom_blocking(matching, arrived, men_prefs, women_prefs)
        if len(matching) == n and is_stable(matching, men_prefs, women_prefs):
            normalized = tuple(sorted(matching.items()))
            reachable_matchings.add(normalized)
            print(len(reachable_matchings))
            if len(reachable_matchings)==8:
                print(count)
                break

    return len(reachable_matchings), reachable_matchings

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








print(count_rom_reachable_matchings_full_rom(men_prefs, women_prefs))
