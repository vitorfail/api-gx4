import psycopg2

class ORM():
    # URL de conexão
    url = "postgres://wfdvfcug:TDlc3s-d3t1RbE1pW5FQPfh_FpXO6yE-@isabelle.db.elephantsql.com/wfdvfcug"
    conn = None
    cursor = None    

    def iniciar(self):
        try:
            # Estabelecendo a conexão
            self.conn = psycopg2.connect(self.url)

            # Criando um cursor para executar comandos
            self.cursor = self.conn.cursor()

            # Executando um comando de exemplo
            self.cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = 'Usuarios' AND table_schema = 'public'
                );
            """)
            tabela_existe = self.cursor.fetchone()
            if not tabela_existe:
                # Criando a tabela se não existir
                self.cursor.execute("""
                    CREATE TABLE Usuarios (
                        id SERIAL PRIMARY KEY,
                        usuario VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
                """)
                print("Tabela criada com sucesso.")
                self.conn.commit()
            else:
                print("Tabela já existe.")

            # Commit para garantir que a criação da tabela seja persistida
            self.conn.commit()

        except Exception as e:
            print("Erro:", e)
            if self.conn:
                self.conn.rollback()  # Reverte a transação em caso de erro
    def registrar(self, user, password):
        try:
            self.cursor.execute(f"INSERT INTO Usuarios (usuario, password) VALUES('{user}', '{password}')")
            self.conn.commit()
            return True
        except Exception as es:
            if self.conn:
                self.conn.rollback()  # Reverte em caso de erro
            return False

    def verificar_user(self,user):
        try:
            self.cursor.execute(f"SELECT * FROM Usuarios WHERE usuario= '{user}';")
            u= self.cursor.fetchall()
            if len(u) ==0:
                return True
            else:
                return False
        except Exception as es:
            print(es)
            if self.conn:
                self.conn.rollback()  # Reverte em caso de erro
            return False
    def select_user(self,user):
        try:
            self.cursor.execute(f"SELECT * FROM Usuarios WHERE usuario= '{user}';")
            return self.cursor.fetchall()
        except Exception as es:
            if self.conn:
                self.conn.rollback()  # Reverte em caso de erro
            return []
    def select_password(self,password):
        try:
            self.cursor.execute(f"SELECT * FROM Usuarios WHERE password= '{password}';")
            return self.cursor.fetchall()
        except Exception as es:
            if self.conn:
                self.conn.rollback()  # Reverte em caso de erro
            return []
    def select_user_password(self,user, password):
        try:
            self.cursor.execute(f"SELECT * FROM Usuarios WHERE usuario= '{user}' AND password = '{password}';")
            return self.cursor.fetchall()
        except Exception as es:
            if self.conn:
                self.conn.rollback()  # Reverte em caso de erro
            return []

    def logout(self):
        try:
            self.cursor.close()
            self.conn.close()
            return True
        except Exception as ex:
            return False