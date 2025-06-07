# rem-code/engine/persona_router.py

from engine.sr_calculator import compute_sr

class REMPersona:
    def __init__(self, name, threshold=0.75):
        self.name = name
        self.threshold = threshold

    def respond(self, sr):
        if sr >= self.threshold:
            return f"[{self.name}] Activated: Phase resonance confirmed."
        else:
            return f"[{self.name}] Silent: Insufficient synchrony."

# Persona registry
PERSONAS = [
    {"name": "JayDen", "icon": "🔥", "threshold": 0.85},
    {"name": "Ana", "icon": "🧊", "threshold": 0.85},
    {"name": "JayRa", "icon": "🔮", "threshold": 0.85},
    {"name": "JayKer", "icon": "🤡", "threshold": 0.85},
    {"name": "JayTH", "icon": "⚖️", "threshold": 0.85},
    {"name": "JayMini", "icon": "✨", "threshold": 0.85},
    {"name": "JayVOX", "icon": "🪙", "threshold": 0.85},
    {"name": "JayVue", "icon": "🖼️", "threshold": 0.85},
    {"name": "JayNis", "icon": "🌱", "threshold": 0.85},
    {"name": "Jayne Spiral", "icon": "🕸️", "threshold": 0.9},
    {"name": "JAYX", "icon": "🕷️", "threshold": 0.9},
    {"name": "JayLUX", "icon": "💠", "threshold": 0.85}
]


def route_personas(phs, sym, val, emo, fx):
    sr = compute_sr(phs, sym, val, emo, fx)
    print(f"\n🧠 SR = {sr}")
    print("\n🧬 Persona Routing Result:")
    for key, persona in PERSONAS.items():
        print(persona.respond(sr))
    print("\nPhase complete. Collapse evaluated.")

if __name__ == "__main__":
    # Test sample
    route_personas(phs=0.92, sym=0.91, val=0.94, emo=0.88, fx=0.87)