import pyodbc
from pathlib import *
from dotenv import load_dotenv

load_dotenv()

###############################################################################################################

def cadastrar_crm(conn, uf, crm):
    dir_atual = Path(__file__).parent
    caminho_arquivo_crm = dir_atual / "CRM_INFO" / f"{uf.upper()}.TXT"
    caminho_script_crm = dir_atual / "ScriptSQL" / "insert_medicos.sql"

    if not caminho_arquivo_crm.exists():
        return f"Arquivo de CRM para o estado '{uf.upper()}' não encontrado.\nVerifique a sigla digitada."

    with open(caminho_script_crm, 'r', encoding='utf-8') as file:
        script_crm = file.read()
    
    nome_medico = None
    with open(caminho_arquivo_crm, 'r', encoding='utf-8') as file:
        for linha in file:
            campos = linha.strip().split("!")
            if len(campos) >= 3 and campos[0] == str(crm):
                nome_medico = campos[2].upper()

                if campos[4] != 'Ativo':
                    return f"Médico com CRM {crm}\nNão Ativo na UF {(uf.upper())}."

                break

    if not nome_medico:
        return f"Médico com CRM {crm}\nNão encontrado na base de dados {(uf.upper())}."

    cursor = conn.cursor()

    try:
        
        cursor.execute("SELECT COUNT(*) FROM MEDICOS WHERE CR = ? AND UF = ?", (crm, uf.upper()))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            return f"Médico: {nome_medico}\nCRM: {crm}\n\nJá cadastrado no estado {uf.upper()}."

        cursor.execute(script_crm, (nome_medico, crm, uf.upper()))
        conn.commit()

        return f"Médico(a) {nome_medico}\n\nCadastrado com sucesso!"

    except pyodbc.Error as e:

        return f"Erro ao inserir médico: {e}"

    finally:
        cursor.close()

###############################################################################################################

#cadastrar_crm('ro', 100297)