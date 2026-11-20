# -*- coding: utf-8 -*-

from conexao import conectar

# únicas funções q importam
def inserir_questao(
    ano,
    disciplina,
    enunciado,
    alternativa_a,
    alternativa_b,
    alternativa_c,
    alternativa_d,
    alternativa_e,
    alternativa_correta,
    imagem_url,
):
    """CREATE"""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO questoes (
                ano, disciplina, enunciado,
                alternativa_a, alternativa_b, alternativa_c,
                alternativa_d, alternativa_e, alternativa_correta, imagem_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                ano,
                disciplina,
                enunciado,
                alternativa_a,
                alternativa_b,
                alternativa_c,
                alternativa_d,
                alternativa_e,
                alternativa_correta,
                imagem_url,
            ),
        )
        conexao.commit()

def sortear_questao():
    """READ aleatório"""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id, ano, disciplina, enunciado, alternativa_a, alternativa_b,
                   alternativa_c, alternativa_d, alternativa_e, alternativa_correta, imagem_url
            FROM questoes
            ORDER BY RAND()
            LIMIT 1
            """
        )
        return cursor.fetchone()

def buscar_questao_por_id(id_questao):
    """READ por ID"""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id, ano, disciplina, enunciado,
                   alternativa_a, alternativa_b, alternativa_c,
                   alternativa_d, alternativa_e, alternativa_correta, imagem_url
            FROM questoes
            WHERE id = %s
            """,
            (id_questao,),
        )
        return cursor.fetchone()

def atualizar_questao(
    id_questao,
    ano,
    disciplina,
    enunciado,
    alternativa_a,
    alternativa_b,
    alternativa_c,
    alternativa_d,
    alternativa_e,
    alternativa_correta,
    imagem_url,
):
    """UPDATE"""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE questoes
            SET ano = %s,
                disciplina = %s,
                enunciado = %s,
                alternativa_a = %s,
                alternativa_b = %s,
                alternativa_c = %s,
                alternativa_d = %s,
                alternativa_e = %s,
                alternativa_correta = %s,
                imagem_url = %s
            WHERE id = %s
            """,
            (
                ano,
                disciplina,
                enunciado,
                alternativa_a,
                alternativa_b,
                alternativa_c,
                alternativa_d,
                alternativa_e,
                alternativa_correta,
                imagem_url,
                id_questao,
            ),
        )
        conexao.commit()
        return cursor.rowcount

def deletar_questao(id_questao):
    """DELETE"""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM questoes WHERE id = %s", (id_questao,))
        conexao.commit()
        return cursor.rowcount