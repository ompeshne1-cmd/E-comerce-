"""
Helper script to configure MySQL credentials and migrate Hedlum database.
Usage:
    python setup_mysql.py
"""
import os
import sys
import pymysql

def configure_mysql():
    print("==================================================")
    print("    HEDLUM E-COMMERCE - MYSQL SETUP WIZARD")
    print("==================================================")
    host = input("Enter MySQL Host [default: localhost]: ").strip() or "localhost"
    port = input("Enter MySQL Port [default: 3306]: ").strip() or "3306"
    user = input("Enter MySQL Username [default: root]: ").strip() or "root"
    password = input("Enter MySQL Password: ").strip()
    db_name = input("Enter Database Name [default: hedlum_db]: ").strip() or "hedlum_db"

    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port)
        )
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4;")
        conn.commit()
        conn.close()
        print(f"\n[+] Successfully created or verified MySQL database '{db_name}'!")
        
        env_content = f"""DB_HOST={host}
DB_PORT={port}
DB_USER={user}
DB_PASSWORD={password}
DB_NAME={db_name}
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("[+] Created .env file with your credentials.")
        print("[+] Applying Django migrations to MySQL...")
        os.system(f"set DB_PASSWORD={password}& set DB_USER={user}& python manage.py migrate")
        print("\n[+] Done! MySQL is fully configured for Hedlum E-Commerce.")
    except Exception as e:
        print(f"\n[-] Error connecting to MySQL: {e}")

if __name__ == "__main__":
    configure_mysql()
