from discord import Locale

translations = {
    "ping": {"test": {Locale.british_english: "Testing ping", 
             Locale.american_english: "Testing ping",
             Locale.french: "Tester le ping"},
        "ping_embed_names": {
            Locale.british_english: ["Bot Latency", "API Latency"],
            Locale.american_english: ["Bot Latency", "API Latency"],
            Locale.french: ["Latence du bot", "Latence de l'API"],
        }
    },
}
