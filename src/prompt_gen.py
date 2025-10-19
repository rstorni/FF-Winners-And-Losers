import random
import time

winning_majesty_tiers = {
        0: {
            "adjectives": ["simple", "plain", "modest", "minimalist", "understated"],
            "atmosphere": [
                "natural lighting, basic composition",
                "soft daylight, straightforward view",
                "clear lighting, simple angle"
            ],
            "quality": ["detailed", "clean", "clear"],
            "extras": ["", "peaceful", "serene", "quiet", "calm"]
        },
        1: {
            "adjectives": ["elegant", "refined", "dignified", "graceful", "noble"],
            "atmosphere": [
                "soft dramatic lighting, balanced composition",
                "golden hour glow, artistic framing",
                "warm lighting, professional photography"
            ],
            "quality": ["highly detailed", "artstation quality", "professional"],
            "extras": ["atmospheric", "sophisticated", "tasteful", "polished", ""]
        },
        2: {
            "adjectives": ["grand", "majestic", "imposing", "magnificent", "glorious", "splendid"],
            "atmosphere": [
                "epic lighting, cinematic composition, golden hour",
                "dramatic sunset, wide angle cinematic shot",
                "sweeping vista, heroic lighting, epic scale"
            ],
            "quality": ["highly detailed", "trending on artstation", "8k", "award winning"],
            "extras": ["breathtaking", "stunning", "powerful", "commanding", "impressive"]
        },
        3: {
            "adjectives": ["awe-inspiring", "legendary", "transcendent", "divine", "ethereal", "mythical", "celestial"],
            "atmosphere": [
                "dramatic god rays, epic cinematic lighting, heavenly atmosphere, volumetric lighting",
                "radiant divine light, celestial beams, otherworldly glow, mystical fog",
                "transcendent illumination, cosmic energy, sacred lighting, angelic rays"
            ],
            "quality": ["masterpiece", "ultra detailed", "trending on artstation", "8k uhd", "unreal engine"],
            "extras": ["sublime", "overwhelming", "supernatural", "godlike", "apocalyptic beauty", "cosmic grandeur"]
        }
    }

losing_majesty_tiers = {
    0: {
        "adjectives": ["pathetic", "pitiful", "miserable", "dejected", "deflated", "woeful"],
        "atmosphere": [
            "harsh fluorescent lighting, empty room, lonely corner, depressing isolation",
            "cold gray morning, empty parking lot, abandoned feeling, nobody cares",
            "dim room lighting, staring at wall, profound sadness, utterly alone"
        ],
        "quality": ["depressingly mundane", "sadly realistic", "uncomfortably detailed", "dreary"],
        "extras": ["heartbreaking", "crushingly ordinary", "profoundly sad", "emotionally drained", "defeated spirit", "given up"]
    },
    1: {
        "adjectives": ["gloomy", "dreary", "dismal", "bleak", "somber", "melancholic"],
        "atmosphere": [
            "overcast skies, muted colors, fading light, heavy fog",
            "perpetual twilight, gray clouds, diminishing hope, shadowy gloom",
            "cold filtered light through clouds, lifeless ambiance, colorless world"
        ],
        "quality": ["moody photography", "depressing atmosphere", "desaturated", "grim detail"],
        "extras": ["oppressive", "joyless", "drained", "weary", "forgotten", "hollow"]
    },
    2: {
        "adjectives": ["dull", "bland", "unremarkable", "mediocre", "forgettable", "mundane"],
        "atmosphere": [
            "flat lighting, uninspired composition, beige tones",
            "fluorescent office lighting, sterile environment, lifeless",
            "overcast afternoon, no shadows, completely average view"
        ],
        "quality": ["acceptable", "passable", "basic quality", "stock photo aesthetic"],
        "extras": ["monotonous", "tedious", "lackluster", "uninspiring", "", "neutral"]
    },
    3: {
        "adjectives": ["slightly worn", "faded", "tired", "weathered", "diminished", "tarnished"],
        "atmosphere": [
            "cloudy day, muted sunlight, past-its-prime",
            "late afternoon overcast, hints of wear, slightly neglected",
            "soft gray light, gentle deterioration, quiet decline"
        ],
        "quality": ["detailed but faded", "lived-in", "showing age", "slightly weathered"],
        "extras": ["melancholy", "wistful", "subdued", "gentle sadness", "bittersweet", "resigned"]
    }
}

def create_majestic_prompt(subject, result, beast_score, seed=None):
    if seed is not None:
        random.seed(seed)

    is_winner = True if result == 'WIN' else False
    beast_score = abs(beast_score)
    majesty_tiers = winning_majesty_tiers if is_winner else losing_majesty_tiers
    majesty_level = max(0, min(15, beast_score)) # Clamp to [0, 15]
    normalized_level = majesty_level / 15.0  # Convert to [0, 1]
    tier_index = normalized_level * 3  # Scale to [0, 3]
    lower_tier = int(tier_index)
    upper_tier = min(lower_tier + 1, 3)
    blend = tier_index - lower_tier
    
    # Select tier based on blend
    if blend < 0.5:
        tier = majesty_tiers[lower_tier]
    else:
        tier = majesty_tiers[upper_tier]
    
    # Randomly select from available options
    adjective = random.choice(tier["adjectives"])
    atmosphere = random.choice(tier["atmosphere"])
    quality = random.choice(tier["quality"])
    extra = random.choice(tier["extras"])
    
    # Build the prompt with random elements
    prompt_parts = [f"{adjective} {subject}", atmosphere, quality]
    
    if extra:  # Only add if extra is not empty
        prompt_parts.insert(1, extra)
    
    prompt = ", ".join(prompt_parts) + ", randomized"
    
    return prompt