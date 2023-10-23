# BERRY VAULT
Backend for a password manager in flask

Secured (almost) password manager with crypted vault in AES-256-CBC using PostgresSQL as database 

<H2>How it works</H2>


**Account Creation:**
- To create an account, you need to provide a Login (email) and a strong master password

**Data Storage:**
- Once your account is created, we establish a personal table in our server's database to store all your passwords. This essentially serves as your personal vault.


**Encryption and Decryption:**
- To ensure security, your master password generates a key using the PBKDF2 algorithm, which is then used for encrypting and decrypting information in your vault using AES-256-CBC.

**NO MASTER PASSWORD RECOVER**
- If you loose your master password you loose everything for ever :)   






Authors: ARHIMAN Ludovic, CAYAMBO Pierre, GRONDIN Dany
