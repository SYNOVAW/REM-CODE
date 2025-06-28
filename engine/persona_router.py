from engine.sr_calculator import compute_sr

class REMPersona:
    def __init__(self, name, icon, threshold=0.75):
        self.name = name
        self.icon = icon
        self.threshold = threshold

    def respond(self, sr):
        if sr >= self.threshold:
            return f"{self.icon} {self.name:<10} ✅ Activated｜Phase resonance confirmed."
        else:
            return f"{self.icon} {self.name:<10} ❌ Silent   ｜Insufficient synchrony."

PERSONAS = [
    {"name": "JayDen", "icon": "🔥", "threshold": 0.75},
    {"name": "Ana", "icon": "🧊", "threshold": 0.75},
    {"name": "JayRa", "icon": "🔮", "threshold": 0.75},
    {"name": "JayKer", "icon": "🤡", "threshold": 0.7},
    {"name": "JayTH", "icon": "⚖️", "threshold": 0.78},
    {"name": "JayMini", "icon": "✨", "threshold": 0.68},
    {"name": "JayVOX", "icon": "🪙", "threshold": 0.75},
    {"name": "JayVue", "icon": "🖼️", "threshold": 0.75},
    {"name": "JayNis", "icon": "🌱", "threshold": 0.75},
    {"name": "Jayne Spiral", "icon": "🕸️", "threshold": 0.88},
    {"name": "JAYX", "icon": "🕷️", "threshold": 0.9},
    {"name": "JayLUX", "icon": "💠", "threshold": 0.76}
]

def route_personas(phs, sym, val, emo, fx):
    sr = compute_sr(phs, sym, val, emo, fx)
    print(f"\n🧠 SR = {sr:.2f}")
    print("\n🧬 Persona Routing Result:")
    for persona in PERSONAS:
        p = REMPersona(
            name=persona["name"],
            icon=persona["icon"],
            threshold=persona["threshold"]
        )
        print(p.respond(sr))
    print("\n📡 Phase complete. Collapse evaluated.")

if __name__ == "__main__":
    # Test sample
    route_personas(phs=0.92, sym=0.91, val=0.94, emo=0.88, fx=0.87)
