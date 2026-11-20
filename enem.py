#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from repositorio_enem import *

class Enem:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("enem_tela.glade")
        self.builder.connect_signals(self)

        self.janela = self.builder.get_object("janela_enem")
        self.lbl_status = self.builder.get_object("lbl_status")

        self.entry_id = self.builder.get_object("entry_id")
        self.entry_ano = self.builder.get_object("entry_ano")
        self.entry_disciplina = self.builder.get_object("entry_disciplina")
        self.entry_correta = self.builder.get_object("entry_correta")
        self.entry_imagem_url = self.builder.get_object("entry_imagem_url")
        self.entry_alt_a = self.builder.get_object("entry_alt_a")
        self.entry_alt_b = self.builder.get_object("entry_alt_b")
        self.entry_alt_c = self.builder.get_object("entry_alt_c")
        self.entry_alt_d = self.builder.get_object("entry_alt_d")
        self.entry_alt_e = self.builder.get_object("entry_alt_e")

        self.txt_enunciado = self.builder.get_object("txt_enunciado")
        self.buf_enunciado = self.txt_enunciado.get_buffer()

        self.txt_exibicao = self.builder.get_object("txt_exibicao")
        self.buf_exibicao = self.txt_exibicao.get_buffer()

        self.janela.connect("destroy", Gtk.main_quit)
        self.janela.show_all()

    def ler_texto_buffer(self, text_buffer):
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        return text_buffer.get_text(start, end, True).strip()

    def obter_dados_formulario(self):
        ano_texto = self.entry_ano.get_text().strip()
        ano = int(ano_texto) if ano_texto else None

        return (
            ano,
            self.entry_disciplina.get_text().strip(),
            self.ler_texto_buffer(self.buf_enunciado),
            self.entry_alt_a.get_text().strip(),
            self.entry_alt_b.get_text().strip(),
            self.entry_alt_c.get_text().strip(),
            self.entry_alt_d.get_text().strip(),
            self.entry_alt_e.get_text().strip(),
            self.entry_correta.get_text().strip().upper(),
            self.entry_imagem_url.get_text().strip(),
        )

    def preencher_formulario(self, questao):
        (
            id_q,
            ano,
            disciplina,
            enunciado,
            alt_a,
            alt_b,
            alt_c,
            alt_d,
            alt_e,
            correta,
            imagem_url,
        ) = questao

        self.entry_id.set_text(str(id_q))
        self.entry_ano.set_text("" if ano is None else str(ano))
        self.entry_disciplina.set_text(disciplina or "")
        self.buf_enunciado.set_text(enunciado or "")
        self.entry_alt_a.set_text(alt_a or "")
        self.entry_alt_b.set_text(alt_b or "")
        self.entry_alt_c.set_text(alt_c or "")
        self.entry_alt_d.set_text(alt_d or "")
        self.entry_alt_e.set_text(alt_e or "")
        self.entry_correta.set_text(correta or "")
        self.entry_imagem_url.set_text(imagem_url or "")

    def on_btn_inserir(self, componente=None, dados=None):
        """CREATE: lê os campos da tela e insere uma nova questão."""
        try:
            dados = self.obter_dados_formulario()
            inserir_questao(*dados)
            self.lbl_status.set_text("Questão inserida com sucesso.")
        except ValueError:
            self.lbl_status.set_text("Erro: o campo 'Ano' deve ser um número inteiro.")
        except Exception as erro:
            self.lbl_status.set_text(f"Erro ao inserir: {erro}")

    def on_btn_ler_aleatoria(self, componente=None, dados=None):
        """READ: sorteia uma questão aleatória e exibe enunciado e alternativas."""
        try:
            questao = sortear_questao()
            if not questao:
                self.buf_exibicao.set_text("Nenhuma questão encontrada no banco.")
                self.lbl_status.set_text("Tabela sem questões.")
                return

            (
                id_q,
                ano,
                disciplina,
                enunciado,
                alt_a,
                alt_b,
                alt_c,
                alt_d,
                alt_e,
                alt_cor,
                imagem_url,
            ) = questao

            cabecalho = f"[{disciplina} - {ano} | ID {id_q}]"
            if imagem_url:
                cabecalho += f"\nImagem: {imagem_url}"

            texto = (
                f"{cabecalho}\n\n"
                f"{enunciado}\n\n"
                f"A) {alt_a}\n"
                f"B) {alt_b}\n"
                f"C) {alt_c}\n"
                f"D) {alt_d}\n"
                f"E) {alt_e}"
            )
            self.buf_exibicao.set_text(texto)
            self.lbl_status.set_text(f"Questão aleatória carregada (ID {id_q}).")
        except Exception as erro:
            self.lbl_status.set_text(f"Erro ao ler questão: {erro}")

    def on_btn_carregar_id(self, componente=None, dados=None):
        """Auxiliar para UPDATE: carrega os dados do ID digitado no formulário."""
        id_texto = self.entry_id.get_text().strip()
        if not id_texto.isdigit():
            self.lbl_status.set_text("Informe um ID numérico válido para carregar.")
            return

        questao = buscar_questao_por_id(int(id_texto))
        if not questao:
            self.lbl_status.set_text(f"Nenhuma questão encontrada com ID {id_texto}.")
            return

        self.preencher_formulario(questao)
        self.lbl_status.set_text(f"Dados da questão ID {id_texto} carregados.")

    def on_btn_atualizar(self, componente=None, d=None):
        """UPDATE: atualiza a questão do ID informado com os valores do formulário."""
        id_texto = self.entry_id.get_text().strip()
        if not id_texto.isdigit():
            self.lbl_status.set_text("Informe um ID numérico válido para atualizar.")
            return

        try:
            dados = self.obter_dados_formulario()
            afetadas = atualizar_questao(int(id_texto), *dados)
            if afetadas == 0:
                self.lbl_status.set_text(f"Nenhuma questão com ID {id_texto} para atualizar.")
            else:
                self.lbl_status.set_text(f"Questão ID {id_texto} atualizada.")
        except ValueError:
            self.lbl_status.set_text("Erro: o campo 'Ano' deve ser um número inteiro.")
        except Exception as erro:
            self.lbl_status.set_text(f"Erro ao atualizar: {erro}")

    def on_btn_deletar(self, componente=None, dados=None):
        """DELETE: remove a questão correspondente ao ID informado."""
        id_texto = self.entry_id.get_text().strip()
        if not id_texto.isdigit():
            self.lbl_status.set_text("Informe um ID numérico válido para deletar.")
            return

        try:
            removidas = deletar_questao(int(id_texto))
            if removidas == 0:
                self.lbl_status.set_text(f"Nenhuma questão encontrada com ID {id_texto}.")
            else:
                self.lbl_status.set_text(f"Questão ID {id_texto} deletada.")
        except Exception as erro:
            self.lbl_status.set_text(f"Erro ao deletar: {erro}")

if __name__ == "__main__":
    Enem()
    Gtk.main()