import sys

# Intentar usar psycopg (v3) primero, si no está disponible usar psycopg2
try:
    import psycopg
    PSYCOPG_VERSION = 3
except ImportError:
    try:
        import psycopg2 as psycopg
        PSYCOPG_VERSION = 2
    except ImportError:
        print("ERROR: No se encontró psycopg ni psycopg2. Instala con: pip install psycopg[binary]")
        sys.exit(1)  # Sale con código de error (1 = falló)

def crear_base_datos():
    """Crea la base de datos 'homecloud' en PostgreSQL"""
    try:
        print("🔌 Conectando al servidor PostgreSQL...")
        # Conectar a la base de datos 'postgres' (base de datos por defecto)
        if PSYCOPG_VERSION == 3:
            # psycopg v3: Azure requiere SSL
            conn = psycopg.connect(
                host="homefamily.postgres.database.azure.com",
                user="administrador",
                password="HomeFamily1.",
                dbname="postgres",
                sslmode="require",
                connect_timeout=10  # Timeout de 10 segundos
            )
        else:
            # psycopg2
            conn = psycopg.connect(
                host="homefamily.postgres.database.azure.com",
                user="administrador",
                password="HomeFamily1.",
                database="postgres",
                sslmode="require",
                connect_timeout=10  # Timeout de 10 segundos
            )
        
        print("✅ Conexión establecida correctamente")
        print("🔍 Verificando si la base de datos ya existe...")
        
        # Habilitar autocommit para poder crear la base de datos
        conn.autocommit = True

        cursor = conn.cursor()
        
        # Verificar si la base de datos ya existe
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = 'homecloud'
        """)
        
        existe = cursor.fetchone()
        
        if existe:
            print("⚠️  La base de datos 'homecloud' ya existe.")
            cursor.close()
            conn.close()
            return True
        
        # Crear la base de datos
        print("📝 Creando la base de datos 'homecloud'...")
        cursor.execute("CREATE DATABASE homecloud;")
        
        # Verificar que se creó correctamente
        print("🔍 Verificando que se creó correctamente...")
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = 'homecloud'
        """)
        
        verificacion = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if verificacion:
            print("✅ Base de datos 'homecloud' creada exitosamente")
            return True
        else:
            print("❌ ERROR: La base de datos no se pudo crear")
            return False
            
    except psycopg.OperationalError as e:
        print(f"\n❌ ERROR de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("  1. Verifica que el servidor PostgreSQL esté accesible")
        print("  2. Verifica que las credenciales sean correctas")
        print("  3. Verifica que el firewall de Azure permita tu IP")
        print("  4. Verifica tu conexión a internet")
        return False
    except psycopg.errors.OperationalError as e:
        # Para psycopg v3, el error puede ser diferente
        print(f"\n❌ ERROR de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("  1. Verifica que el servidor PostgreSQL esté accesible")
        print("  2. Verifica que las credenciales sean correctas")
        print("  3. Verifica que el firewall de Azure permita tu IP")
        print("  4. Verifica tu conexión a internet")
        return False
    except psycopg.ProgrammingError as e:
        if "already exists" in str(e).lower():
            print("⚠️  La base de datos 'homecloud' ya existe.")
            return True
        else:
            print(f"❌ ERROR de SQL: {e}")
            return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Intentando crear la base de datos 'homecloud'...")
    print(f"📦 Usando psycopg versión {PSYCOPG_VERSION}")
    print("-" * 50)
    
    exito = crear_base_datos()
    
    print("-" * 50)
    if exito:
        print("✅ Proceso completado exitosamente")
        sys.exit(0) # Sale con código de éxito (0 = OK)
    else:
        print("❌ El proceso falló")
        sys.exit(1) # Sale con código de error (1 = falló)
