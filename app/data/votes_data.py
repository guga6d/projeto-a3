ASSETS_FOLDER = "assets/images"


PRIMARY_QUESTIONS = [
    {
        "id": "travel_style",
        "question": "O que você mais gosta de fazer nas férias?",
        "options": [
            {
                "label": "Relaxar",
                "icon": f"{ASSETS_FOLDER}/icon_rest.png",
                "description": "Descansar e recarregar",
            },
            {
                "label": "Aventuras",
                "icon": f"{ASSETS_FOLDER}/icon_mountain.png",
                "description": "Viver emoções e explorar",
            },
            {
                "label": "Cultura / Explorar",
                "icon": f"{ASSETS_FOLDER}/icon_cultural.png",
                "description": "Conhecer lugares e suas histórias",
            },
        ],
    }
]


SECONDARY_QUESTION = {
    "id": "travel_company",
    "question": "Com quem você prefere viajar?",
    "options": [
        {
            "label": "Família / Casal",
            "icon": f"{ASSETS_FOLDER}/icon_family.png",
            "description": "Momentos inesquecíveis juntos",
        },
        {
            "label": "Amigos",
            "icon": f"{ASSETS_FOLDER}/icon_friends.png",
            "description": "Diversão garantida",
        },
        {
            "label": "Sozinho(a)",
            "icon": f"{ASSETS_FOLDER}/icon_alone.png",
            "description": "Sua própria companhia e liberdade",
        },
    ],
}


# Mapeamento direto (estilo, companhia) → 3 destinos com metadados prontos
# (name + image + description). Não precisa de função para montar o meta:
# o serviço lê diretamente daqui.
DESTINATIONS_BY_ANSWERS = {
    "Relaxar": {
        "Amigos": [
            {
                "name": "Florianópolis - SC",
                "image": f"{ASSETS_FOLDER}/florianopolis.png",
                "description": "Praias e vibe leve",
            },
            {
                "name": "Arraial do Cabo - RJ",
                "image": f"{ASSETS_FOLDER}/arraial_do_cabo.png",
                "description": "Mar cristalino e sossego",
            },
            {
                "name": "Tulum - México",
                "image": f"{ASSETS_FOLDER}/tulum.png",
                "description": "Praia e estilo boho",
            },
        ],
        "Sozinho(a)": [
            {
                "name": "Ubatuba - SP",
                "image": f"{ASSETS_FOLDER}/ubatuba.png",
                "description": "Natureza e tranquilidade",
            },
            {
                "name": "Campos do Jordão - SP",
                "image": f"{ASSETS_FOLDER}/campos_do_jordao.png",
                "description": "Refúgio e silêncio",
            },
            {
                "name": "Ubud - Bali, Indonésia",
                "image": f"{ASSETS_FOLDER}/ubud.png",
                "description": "Espiritualidade e paz",
            },
        ],
        "Família / Casal": [
            {
                "name": "Porto Seguro - BA",
                "image": f"{ASSETS_FOLDER}/porto_seguro.png",
                "description": "Praia tranquila e descanso",
            },
            {
                "name": "Gramado - RS",
                "image": f"{ASSETS_FOLDER}/gramado.png",
                "description": "Clima aconchegante e romance",
            },
            {
                "name": "Cancún - México",
                "image": f"{ASSETS_FOLDER}/cancun.png",
                "description": "Resorts e relax total",
            },
        ],
    },

    "Aventuras": {
        "Amigos": [
            {
                "name": "Fernando de Noronha - PE",
                "image": f"{ASSETS_FOLDER}/fernando_de_noronha.png",
                "description": "Mergulho e paisagens",
            },
            {
                "name": "Rio de Janeiro - RJ",
                "image": f"{ASSETS_FOLDER}/rio_de_janeiro.png",
                "description": "Trilhas e praia",
            },
            {
                "name": "Interlaken - Suíça",
                "image": f"{ASSETS_FOLDER}/interlaken.png",
                "description": "Esportes radicais e montanhas",
            },
        ],
        "Sozinho(a)": [
            {
                "name": "Chapada Diamantina - BA",
                "image": f"{ASSETS_FOLDER}/chapada_diamantina.png",
                "description": "Trilhas e cachoeiras",
            },
            {
                "name": "Cusco - Peru",
                "image": f"{ASSETS_FOLDER}/cusco.png",
                "description": "História e aventura",
            },
            {
                "name": "Queenstown - Nova Zelândia",
                "image": f"{ASSETS_FOLDER}/queenstown.png",
                "description": "Adrenalina e natureza",
            },
        ],
        "Família / Casal": [
            {
                "name": "Bonito - MS",
                "image": f"{ASSETS_FOLDER}/bonito.png",
                "description": "Ecoturismo e águas cristalinas",
            },
            {
                "name": "Foz do Iguaçu - PR",
                "image": f"{ASSETS_FOLDER}/foz_do_iguacu.png",
                "description": "Cataratas e passeios",
            },
            {
                "name": "Orlando - EUA",
                "image": f"{ASSETS_FOLDER}/orlando.png",
                "description": "Parques e diversão",
            },
        ],
    },

    "Cultura / Explorar": {
        "Amigos": [
            {
                "name": "Barcelona - Espanha",
                "image": f"{ASSETS_FOLDER}/barcelona.png",
                "description": "Cultura e vida noturna",
            },
            {
                "name": "Lisboa - Portugal",
                "image": f"{ASSETS_FOLDER}/lisboa.png",
                "description": "História e gastronomia",
            },
            {
                "name": "Berlim - Alemanha",
                "image": f"{ASSETS_FOLDER}/berlim.png",
                "description": "Arte e modernidade",
            },
        ],
        "Sozinho(a)": [
            {
                "name": "Kyoto - Japão",
                "image": f"{ASSETS_FOLDER}/kyoto.png",
                "description": "Tradição e contemplação",
            },
            {
                "name": "Praga - República Tcheca",
                "image": f"{ASSETS_FOLDER}/praga.png",
                "description": "História e charme",
            },
            {
                "name": "Atenas - Grécia",
                "image": f"{ASSETS_FOLDER}/atenas.png",
                "description": "Filosofia e antiguidade",
            },
        ],
        "Família / Casal": [
            {
                "name": "Salvador - BA",
                "image": f"{ASSETS_FOLDER}/salvador.png",
                "description": "Cultura e história",
            },
            {
                "name": "Roma - Itália",
                "image": f"{ASSETS_FOLDER}/roma.png",
                "description": "História e arquitetura",
            },
            {
                "name": "Paris - França",
                "image": f"{ASSETS_FOLDER}/paris.png",
                "description": "Arte e romance",
            },
        ],
    },
}
