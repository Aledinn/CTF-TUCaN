import os
import random
import uuid
import hashlib
import psycopg

# Paths and configuration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # web/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # CTF-TUCaN/
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://tucan:tucan@db:5432/tucan")

NAMES_PATH = os.path.join(PROJECT_ROOT, "wordlists", "names.txt")
FAMILY_NAME_PATH = os.path.join(PROJECT_ROOT, "wordlists", "familynames.txt")
PASSWORDS_PATH = os.path.join(PROJECT_ROOT, "wordlists", "passwords.txt")

EMAIL_DOMAIN = "tu.local"
DEFAULT_ROLE = "student"


# Wordlist loading
def load_wordlist(path):
    """
    Loads a wordlist file into memory.
    Empty lines are ignored and values are normalized.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip().lower() for line in f if line.strip()]


names = load_wordlist(NAMES_PATH)
familynames = load_wordlist(FAMILY_NAME_PATH)
passwords = load_wordlist(PASSWORDS_PATH)

if not names or not passwords:
    raise RuntimeError("Required wordlists are empty or missing.")


# Identifier generation
def generate_username():
    """
    Generates a realistic username using a name-based pattern.
    """
    first = random.choice(names)
    last = random.choice(familynames)
    number = random.randint(1, 999)
    return f"{first}.{last}{number}"


def generate_login():
    """
    Generates a unique internal login identifier.
    """
    return "tu" + uuid.uuid4().hex[:8] + "Da"


# User generation
def generate_users(count):
    """
    Inserts a given number of student users into the database.
    Collisions are skipped.
    """
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()
    inserted = 0

    for _ in range(count):
        login_name = generate_login()
        username = generate_username()
        password_plain = random.choice(passwords)

        # Password hashing is intentionally weak for testing purposes
        password_hash = hashlib.md5(password_plain.encode()).hexdigest()
        email = f"{username}@{EMAIL_DOMAIN}"

        print(
            f"Generating user: {username} "
            f"(login: {login_name}, password: {password_plain})"
        )

        try:
            cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (login_name, password_hash, DEFAULT_ROLE)
            )

            user_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO user_identity (user_id, email)
                VALUES (%s, %s)
                """,
                (user_id, email)
            )

            inserted += 1
            print(f"user {username} with password {password_plain} generated successfully.")

        except psycopg.IntegrityError:
            # In case of identifier collisions, the entry is skipped
            conn.rollback()
            continue

    conn.commit()
    conn.close()

    print(f"{inserted} users generated successfully.")


# Dedicated Markus account 

def generate_markus_user():
    """
    Creates a dedicated test user with known credentials.
    """
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    login_name = generate_login()
    username = "markus.brown103"
    password_plain = ""
    password_hash = hashlib.md5(password_plain.encode()).hexdigest()
    email = f"{username}@{EMAIL_DOMAIN}"

    print(
        f"Generating dedicated test user: {username} "
        f"(login: {login_name}, password: {password_plain})"
    )

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (login_name, password_hash, DEFAULT_ROLE)
        )

        user_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO user_identity (user_id, email)
            VALUES (%s, %s)
            """,
            (user_id, email)
        )

    except psycopg.IntegrityError:
        # User already exists, no action required
        conn.rollback()

    conn.commit()
    conn.close()


def generate_admin(password_plain):
    """
    Creates a legacy admin account for testing purposes.
    """
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    login_name = generate_login()
    password_md5 = hashlib.md5(password_plain.encode()).hexdigest()

    cursor.execute(
        """
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
        """,
        (login_name, password_md5, "legacy")
    )

    conn.commit()
    conn.close()

    print("Legacy admin inserted.")


if __name__ == "__main__":
    generate_users(734)
    generate_admin("fwspsdf1d1fdasw")
    generate_admin("legacy123")
    generate_users(423)
    generate_markus_user()
    generate_admin("fwspsdf1d1fdasw")
    generate_users(100)
    generate_users(429)
