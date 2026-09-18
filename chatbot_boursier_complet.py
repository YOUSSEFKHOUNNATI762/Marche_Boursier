"""
============================================================================
 CHATBOT BOURSIER - FICHIER COMBINÉ (app.py + requirements.txt + README.md)
============================================================================
Ce fichier unique regroupe l'ensemble du projet pour faciliter le partage :

    1) README.md          -> Documentation et instructions (en commentaire)
    2) requirements.txt   -> Dépendances du projet (en commentaire)
    3) app.py              -> Code source de l'application Streamlit (ci-dessous)

Pour utiliser le projet correctement, il est recommandé de séparer à nouveau
ces 3 sections dans leurs fichiers respectifs (app.py, requirements.txt,
README.md). Ce fichier combiné sert uniquement de référence/archive unique.
============================================================================
"""

############################################################################
# SECTION 1 : README.md
############################################################################
#
# # Chatbot Boursier - Application Streamlit
#
# ## Installation
#
# ```bash
# pip install -r requirements.txt
# ```
#
# ## Lancement
#
# ```bash
# streamlit run app.py
# ```
#
# ## Identifiants de démonstration
#
# - **Utilisateur** : admin
# - **Mot de passe** : bourse2026
#
# ## Fonctionnalités
#
# - Page de connexion sécurisée (session_state)
# - Interface de chat moderne (st.chat_message / st.chat_input)
# - Dashboard boursier simulé (statut du marché, indice MASI, volatilité)
# - Raccourcis de questions fréquentes dans la barre latérale
# - Glossaire express des termes boursiers (accordéon)
# - Design personnalisé avec palette financière (bleu nuit / vert boursier)
#
############################################################################


############################################################################
# SECTION 2 : requirements.txt
############################################################################
#
# streamlit>=1.32.0
# nltk>=3.8.1
#
############################################################################


############################################################################
# SECTION 3 : app.py  (CODE SOURCE PRINCIPAL - COMMENCE CI-DESSOUS)
############################################################################

import random
from datetime import datetime

import nltk
from nltk.chat.util import Chat, reflections
import streamlit as st

# ============================================================================
# 1. CONFIGURATION GÉNÉRALE DE LA PAGE
# ============================================================================
# doit être le premier appel Streamlit du script
st.set_page_config(
    page_title="Chatbot Boursier | Apprentissage Marché Financier",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# 2. IDENTIFIANTS DE DÉMONSTRATION (AUTHENTIFICATION)
# ============================================================================
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "bourse2026"

# ============================================================================
# 3. PAIRES DE DIALOGUES NLTK (reprises et enrichies du code de départ)
# ============================================================================
pairs = [
    [r"mon nom est (.*)",
     ["Hello %1, bienvenue sur le module d'apprentissage du marché boursier !"]],

    [r"bonjour|salut|coucou",
     ["Salut toi, prêt à parler de la bourse et des marchés ?",
      "Hello, vous avez des questions sur la bourse ?"]],

    [r"(.*)c'est quoi(.*)action|(.*)définition(.*)action",
     ["Une action représente une part du capital d'une entreprise. "
      "En l'achetant, vous devenez copropriétaire d'une partie de la société."]],

    [r"(.*)c'est quoi(.*)obligation|(.*)définition(.*)obligation",
     ["Une obligation est un titre de créance. En l'achetant, vous prêtez "
      "de l'argent à une entreprise ou un État en échange d'intérêts réguliers."]],

    [r"(.*)c'est quoi(.*)bourse|(.*)définition(.*)bourse",
     ["La bourse est un marché financier où s'échangent des titres financiers, "
      "comme des actions et des obligations."]],

    [r"(.*)dividende(.*)",
     ["Un dividende est la part des bénéfices nets d'une entreprise distribuée "
      "aux actionnaires."]],

    [r"(.*)indice boursier|(.*)masi(.*)|(.*)indice(.*)",
     ["Un indice boursier mesure la performance globale d'un groupe d'actions "
      "(ex : CAC 40 en France, S&P 500 aux USA, MASI au Maroc)."]],

    [r"(.*)volatilité|(.*)volatil(.*)",
     ["La volatilité mesure l'ampleur des variations du cours d'un actif financier. "
      "Une forte volatilité signifie un risque plus élevé."]],

    [r"(.*)comment acheter(.*)|(.*)acheter(.*)action|(.*)investir(.*)",
     ["Pour acheter des actions, vous devez ouvrir un compte (ex : PEA, Compte-Titres) "
      "auprès d'une banque ou d'un courtier en ligne, puis passer un ordre d'achat."]],

    [r"(.*)ordre au marché|(.*)ordre à la tout venante(.*)",
     ["Un ordre au marché est exécuté immédiatement au meilleur prix disponible, "
      "sans limite de prix fixe."]],

    [r"(.*)bull market|(.*)marché haussier(.*)",
     ["Un 'Bull Market' désigne un marché orienté à la hausse sur une période prolongée."]],

    [r"(.*)bear market|(.*)marché baissier(.*)",
     ["Un 'Bear Market' désigne un marché orienté à la baisse sur une période prolongée."]],

    [r"(.*)risque(.*)",
     ["Investir en bourse comporte toujours un risque de perte en capital. "
      "Il est conseillé de diversifier son portefeuille."]],

    [r"merci(.*)",
     ["De rien ! Bons investissements !"]],

    [r"au revoir|bye|quitter",
     ["Au revoir ! À bientôt sur les marchés !"]],

    [r"(.*)",
     ["Je ne comprends pas, posez-moi une question sur le marché boursier "
      "(actions, obligations, indices, dividendes...)."]],
]

# Instanciation unique du moteur NLTK (mis en cache pour éviter de le
# reconstruire à chaque interaction utilisateur)
@st.cache_resource
def get_chat_engine():
    """Initialise et met en cache le moteur de chat NLTK."""
    return Chat(pairs, reflections)


chat_engine = get_chat_engine()


def get_bot_response(user_text: str) -> str:
    """Retourne la réponse du chatbot NLTK pour un message donné."""
    response = chat_engine.respond(user_text)
    if not response:
        response = "Je ne comprends pas, pouvez-vous reformuler votre question ?"
    return response


# ============================================================================
# 4. CSS PERSONNALISÉ (PALETTE FINANCIÈRE + STYLE DES CARTES)
# ============================================================================
CUSTOM_CSS = """
<style>
    /* ---------- Palette de couleurs ---------- */
    :root {
        --bleu-nuit: #0f172a;
        --vert-boursier: #10b981;
        --gris-clair: #f8fafc;
        --rouge-baisse: #ef4444;
    }

    /* ---------- Masquer les éléments natifs superflus ---------- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- Fond général de l'application ---------- */
    .stApp {
        background-color: var(--gris-clair);
    }

    /* ---------- Titre principal ---------- */
    .main-header {
        background: linear-gradient(135deg, var(--bleu-nuit) 0%, #1e293b 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }
    .main-header p {
        color: #cbd5e1;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    /* ---------- Cartes génériques (bords arrondis + ombre légère) ---------- */
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
    }
    div[data-testid="stMetric"] label {
        color: var(--bleu-nuit) !important;
        font-weight: 600;
    }

    /* ---------- Boutons ---------- */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background-color: white;
        color: var(--bleu-nuit);
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: var(--vert-boursier);
        color: white;
        border-color: var(--vert-boursier);
    }

    /* ---------- Formulaire de connexion (carte centrée) ---------- */
    .login-card {
        background-color: white;
        border-radius: 18px;
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15);
        border: 1px solid #e2e8f0;
        max-width: 420px;
        margin: 3rem auto 0 auto;
    }
    .login-card h2 {
        color: var(--bleu-nuit);
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .login-card p {
        text-align: center;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: var(--bleu-nuit);
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #1e293b;
        border: 1px solid #334155;
        color: #f8fafc !important;
        width: 100%;
        text-align: left;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--vert-boursier);
        border-color: var(--vert-boursier);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================================
# 5. INITIALISATION DE LA SESSION (ÉTAT PARTAGÉ)
# ============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Bonjour et bienvenue sur le module d'apprentissage du marché "
                "boursier ! 📈 Posez-moi une question sur les actions, les "
                "obligations, les indices ou toute autre notion financière."
            ),
        }
    ]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================================
# 6. PAGE DE CONNEXION (LOGIN)
# ============================================================================
def show_login_page():
    """Affiche un formulaire de connexion centré et stylisé."""
    st.markdown(
        """
        <div class="login-card">
            <h2>🔐 Connexion</h2>
            <p>Veuillez vous authentifier pour accéder au Chatbot Boursier</p>
        """,
        unsafe_allow_html=True,
    )

    # Utilisation de colonnes pour centrer visuellement le formulaire
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Utilisateur", placeholder="admin")
            password = st.text_input(
                "Mot de passe", type="password", placeholder="••••••••"
            )
            submitted = st.form_submit_button("Se connecter", use_container_width=True)

            if submitted:
                if username == DEMO_USERNAME and password == DEMO_PASSWORD:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error(
                        "❌ Identifiant ou mot de passe incorrect. "
                        "Veuillez réessayer."
                    )

        st.caption("💡 Identifiants de démonstration : **admin** / **bourse2026**")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# 7. DASHBOARD BOURSIER (WIDGET MARCHÉ EN HAUT DE PAGE)
# ============================================================================
def show_market_header():
    """Affiche l'en-tête dynamique avec les métriques simulées du marché."""
    st.markdown(
        """
        <div class="main-header">
            <h1>📈 Chatbot - Marché Boursier</h1>
            <p>Votre assistant intelligent pour apprendre les bases de la bourse et de l'investissement</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📅 Date", value=datetime.now().strftime("%d/%m/%Y"))
    with col2:
        st.metric(label="🏦 Statut du Marché", value="Ouvert 🟢")
    with col3:
        st.metric(label="📊 Indice MASI", value="12 450 pts", delta="+0.45 %")
    with col4:
        st.metric(label="⚡ Volatilité", value="Modérée")


# ============================================================================
# 8. BARRE LATÉRALE (RACCOURCIS + GLOSSAIRE + DÉCONNEXION)
# ============================================================================
QUICK_QUESTIONS = [
    "C'est quoi une action ?",
    "Définition du MASI ?",
    "Comment acheter des actions ?",
    "C'est quoi une obligation ?",
    "Qu'est-ce que la volatilité ?",
]

GLOSSARY = {
    "Action": "Titre représentant une part du capital d'une entreprise, donnant "
               "droit à une fraction des bénéfices (dividendes) et un droit de vote.",
    "Obligation": "Titre de créance : l'investisseur prête de l'argent à une "
                  "entreprise ou un État en échange d'intérêts réguliers.",
    "Dividende": "Part des bénéfices nets d'une entreprise redistribuée aux "
                 "actionnaires, généralement de façon annuelle.",
    "Bull Market": "Marché haussier : période durant laquelle les cours des "
                   "actifs financiers sont globalement en hausse.",
    "Bear Market": "Marché baissier : période durant laquelle les cours des "
                   "actifs financiers sont globalement en baisse.",
}


def show_sidebar():
    """Construit la barre latérale interactive."""
    with st.sidebar:
        st.markdown("## 👤 Session")
        st.write(f"Connecté en tant que : **{DEMO_USERNAME}**")

        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

        st.divider()

        st.markdown("## 💬 Questions fréquentes")
        st.caption("Cliquez pour envoyer directement la question au chatbot")
        for question in QUICK_QUESTIONS:
            if st.button(question, key=f"quick_{question}", use_container_width=True):
                st.session_state.pending_question = question

        st.divider()

        st.markdown("## 📖 Glossaire express")
        with st.expander("Voir les définitions clés"):
            for term, definition in GLOSSARY.items():
                st.markdown(f"**{term}** : {definition}")


# ============================================================================
# 9. INTERFACE DE CHAT (STYLE CHATGPT / WHATSAPP)
# ============================================================================
def show_chat_interface():
    """Affiche l'historique de conversation et gère les nouveaux messages."""
    st.markdown("### 💬 Discutez avec l'assistant")

    # Affichage de l'historique des messages
    for message in st.session_state.messages:
        avatar = "🧑‍💼" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Priorité à une question issue d'un raccourci de la sidebar
    user_prompt = None
    if st.session_state.pending_question:
        user_prompt = st.session_state.pending_question
        st.session_state.pending_question = None

    # Sinon, on utilise la saisie libre de l'utilisateur
    typed_prompt = st.chat_input("Posez votre question sur la bourse...")
    if typed_prompt:
        user_prompt = typed_prompt

    if user_prompt:
        # Ajout et affichage du message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(user_prompt)

        # Génération et affichage de la réponse du chatbot
        bot_reply = get_bot_response(user_prompt)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(bot_reply)


# ============================================================================
# 10. POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
# ============================================================================
def main():
    if not st.session_state.logged_in:
        # Utilisateur non authentifié -> on masque toute l'application
        show_login_page()
    else:
        # Utilisateur authentifié -> affichage complet de l'application
        show_sidebar()
        show_market_header()
        st.divider()
        show_chat_interface()


if __name__ == "__main__":
    main()
