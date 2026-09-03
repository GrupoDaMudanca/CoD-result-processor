def get_rank_from_sr(sr: int) -> str:
    if sr < 600:
        return "Bronze I"
    elif sr < 700:
        return "Bronze II"
    elif sr < 800:
        return "Bronze III"
    elif sr < 866:
        return "Prata I"
    elif sr < 933:
        return "Prata II"
    elif sr < 1000:
        return "Prata III"
    elif sr < 1066:
        return "Ouro I"
    elif sr < 1133:
        return "Ouro II"
    elif sr < 1200:
        return "Ouro III"
    elif sr < 1266:
        return "Platina I"
    elif sr < 1333:
        return "Platina II"
    elif sr < 1400:
        return "Platina III"
    elif sr < 1500:
        return "Diamante I"
    elif sr < 1600:
        return "Diamante II"
    elif sr < 1700:
        return "Diamante III"
    elif sr < 1766:
        return "Carmesim I"
    elif sr < 1833:
        return "Carmesim II"
    elif sr < 1900:
        return "Carmesim III"
    else:
        return "Iridescente"

def calculate_sr_and_rank(wins: int, objectives: int) -> tuple[int, str, float]:
    """
    Calculates SR, applies objective-based ceilings (gatekeepers), 
    and returns (final_sr, rank_emoji_and_name, multiplier).
    """
    base_sr = 500
    gross_sr = base_sr + (wins * 30) + (objectives * 40)
    
    # Gatekeeper ceilings based on objectives
    if objectives < 4:
        final_sr = min(gross_sr, 1199)
    elif objectives < 8:
        final_sr = min(gross_sr, 1399)
    elif objectives < 12:
        final_sr = min(gross_sr, 1699)
    elif objectives < 16:
        final_sr = min(gross_sr, 1899)
    else:
        final_sr = gross_sr

    multiplier = round(final_sr / 1000.0, 1)
    rank = get_rank_from_sr(final_sr)
        
    return final_sr, rank, multiplier
