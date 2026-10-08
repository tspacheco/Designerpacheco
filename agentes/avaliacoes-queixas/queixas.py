"""Deteta nas avaliações (romeno) as queixas que a IA resolve: telefone sem resposta, mensagens sem resposta,
marcações/encomendas que falham. Usado pelo lista.py; pode correr sozinho para testar uma frase:
  python3 queixas.py "Nu răspund la telefon niciodată"
"""
import re, sys, unicodedata


def plano(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("ţ", "t").replace("ş", "s")


# Ordem = prioridade (a primeira dor encontrada é a que a mensagem cita).
DORES = {
    "telefon": [
        r"\b(nu|n-?au|n-?a|nimeni nu)\s+(mai\s+)?(raspun\w*|preia\w*|ridica\w*)\b[^.!?]{0,40}\btelefon",
        r"\btelefon\w*\b[^.!?]{0,50}\b(nu|n-?a|nimeni nu|fara)\s+(mai\s+)?(raspun\w*|preia\w*|ridica\w*|raspuns)",
        r"\btelefon\w*\s+(\w+\s+){0,3}(inchis|ocupat)\b",
        r"\bla telefon\b[^.!?]{0,30}\b(asteptat|asteapta)\b|\b(asteptat|asteapta)\b[^.!?]{0,30}\bla telefon\b",
        r"\b(am\s+)?sunat\b[^.!?]{0,60}\b(nu|nimeni|niciun|fara)\b[^.!?]{0,30}\b(raspun\w*|raspuns|preia\w*)",
        r"\bsun(at|i|am)?\s+de\s+\d+\s+ori\b",
        r"\b(imposibil|greu|nu am putut|n-am putut|nu se poate)\b[^.!?]{0,25}\b(contacta\w*|lua legatura|da de ei|suna)",
        r"\bnu\s+raspunde\s+nimeni\b",
    ],
    "mesaje": [
        r"\b(mesaj\w*|whatsapp|e-?mail\w*|facebook|instagram|messenger)\b[^.!?]{0,60}\b(nu|n-?au|n-?a|fara|niciun)\b[^.!?]{0,20}\b(raspun\w*|raspuns)",
        r"\b(nu|n-?au|n-?a)\s+(mai\s+)?(raspuns|raspund\w*)\b[^.!?]{0,30}\b(mesaj\w*|whatsapp|e-?mail|facebook|instagram)",
        r"\b(niciun|nici un|fara)\s+raspuns\b",
        r"\b(seen|vazut mesajul)\b[^.!?]{0,30}\bnu\b",
        r"\braspund\w*\s+(foarte\s+)?(greu|tarziu|dupa \w+ zile)",
    ],
    "marcacoes": [
        r"\bprogramar\w*\b[^.!?]{0,60}\b(anulat\w*|uitat\w*|pierdut\w*|nu (a|au) (fost )?(respectat\w*|trecut\w*|notat\w*)|incurcat\w*|greseal\w*)",
        r"\b(anulat\w*|uitat\w*|incurcat\w*)\b[^.!?]{0,40}\bprogramar\w*",
        r"\b(greu|imposibil|nu am reusit|n-am reusit)\b[^.!?]{0,30}\b(programa\w*|programare)",
        r"\bdesi (aveam|am avut) programare\b",
        r"\bcomand\w*\b[^.!?]{0,50}\b(gresit\w*|uitat\w*|pierdut\w*|nu (a|au) (venit|ajuns)|incurcat\w*)",
    ],
}
REGEX = {d: [re.compile(p) for p in ps] for d, ps in DORES.items()}
NOME = {"telefon": "telefone sem resposta", "mesaje": "mensagens sem resposta", "marcacoes": "marcações/encomendas que falham"}


def dores(texto):
    """Devolve [(dor, frase)] por ordem de prioridade; frase = a frase original que bateu."""
    frases = [f.strip() for f in re.split(r"(?<=[.!?])\s+|\n+", texto) if f.strip()]
    achadas = []
    for dor, regs in REGEX.items():
        for f in frases:
            if any(r.search(plano(f)) for r in regs):
                achadas.append((dor, f))
                break
    return achadas


if __name__ == "__main__":
    for d, f in dores(" ".join(sys.argv[1:])):
        print(d, "→", f)
