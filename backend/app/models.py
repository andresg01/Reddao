# Base de datos en memoria para simular un ecosistema REDDAO completo.
db = {
    "users": {
        "andres": {
            "password": "123", "user_type": "user", "wallet_id": "wallet_andres", 
            "nft_id": "nft_user_andres", "center_id": "centro-a", "reputation": 112
        },
        "david": {
            "password": "123", "user_type": "user", "wallet_id": "wallet_david", 
            "nft_id": "nft_user_david", "center_id": "centro-b", "reputation": 95
        },
        "sara_emp": {
            "password": "123", "user_type": "employee", "wallet_id": "wallet_sara_emp",
            "nft_id": "nft_employee_sara", "center_id": "centro-a", "job_title": "Entrenadora de Pádel", "rating": 4.8, "tips_received": 15.5
        },
        "jorge_inv": {
            "password": "123", "user_type": "investor", "wallet_id": "wallet_jorge_inv",
            "nft_id": "nft_investor_jorge", "investments": {"centro-a": 5000}
        },
        "pro_clean": {
            "password": "123", "user_type": "provider", "wallet_id": "wallet_pro_clean",
            "nft_id": "nft_provider_proclean", "service_type": "Limpieza y Mantenimiento"
        },
        "ana_admin": {
            "password": "123", "user_type": "center_admin", "wallet_id": "wallet_centro_a",
            "nft_id": "nft_admin_ana", "center_id": "centro-a"
        }
    },
    "centers": {
        "centro-a": {
            "name": "Metropolitan Padel Club", "owner_wallet": "wallet_centro_a", 
            "services": {"Pista de Pádel": 2.5, "Clase de Pádel": 5, "Gimnasio": 1},
            "employees": { "sara_emp": {"name": "Sara", "job": "Entrenadora", "wallet": "wallet_sara_emp"} },
            "stats": {"monthly_revenue": 1250.75, "active_users": 150}
        },
        "centro-b": {
            "name": "GoFit Yoga & Wellness", "owner_wallet": "wallet_centro_b", 
            "services": {"Clase de Yoga": 2, "Acceso Spa": 4, "Gimnasio": 1},
            "employees": {},
            "stats": {"monthly_revenue": 850.20, "active_users": 85}
        }
    },
    "proposals": {
        "prop_1": {
            "id": "prop_1", "title": "Instalar nuevas luces LED en las pistas de pádel",
            "description": "Propuesta para mejorar la iluminación de las pistas 1 y 2 para los partidos nocturnos. El coste estimado es de 500 RDT.",
            "creator": "wallet_andres", "status": "active",
            "votes": {"yes": 80, "no": 10}, "voters": ["wallet_andres", "wallet_jorge_inv"]
        },
        "prop_2": {
            "id": "prop_2", "title": "Ampliar el horario del Spa los fines de semana",
            "description": "Se propone que el Spa del centro GoFit abra hasta las 22:00 los sábados y domingos.",
            "creator": "wallet_david", "status": "active",
            "votes": {"yes": 50, "no": 0}, "voters": ["wallet_david"]
        }
    },
    "wallets": {
        "reddao_business_wallet": {"balance": 10000, "type": "business"},
        "reddao_marketing_wallet": {"balance": 0, "type": "marketing"},
        "wallet_centro_a": {"balance": 1000, "type": "center"},
        "wallet_centro_b": {"balance": 1000, "type": "center"},
        "wallet_andres": {"balance": 100, "type": "user"},
        "wallet_david": {"balance": 150, "type": "user"},
        "wallet_sara_emp": {"balance": 25.5, "type": "employee"},
        "wallet_jorge_inv": {"balance": 5000, "type": "investor"},
        "wallet_pro_clean": {"balance": 200, "type": "provider"},
    },
    "marketplace": {
        "item_1": {"name": "Bote de Pelotas Pro", "price": 3, "stock": 50, "image": "https://placehold.co/400x400/3B82F6/FFFFFF?text=Bolas"},
        "item_2": {"name": "Toalla Microfibra REDDAO", "price": 5, "stock": 100, "image": "https://placehold.co/400x400/10B981/FFFFFF?text=Toalla"},
        "item_3": {"name": "Sesión de Fisioterapia", "price": 15, "stock": 10, "image": "https://placehold.co/400x400/EF4444/FFFFFF?text=Fisio"}
    }
}
