from models import Pessoas, Atividades, db_session


def insere_pessoas():
    pessoa = Pessoas(nome='Neto', idade='26')
    print(pessoa)
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)
    pessoa = Pessoas.query.filter_by(nome='Nilson').first()
    print(pessoa.idade)


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Nilson').first()
    pessoa.idade = 26
    pessoa.save()


def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Cunha').first()
    pessoa.delete()

def consulta_atividade():
    atividade = Atividades.query.all()
    print(atividade)


if __name__ == '__main__':
    #insere_pessoas()
    #altera_pessoa()
    #exclui_pessoa()
    consulta_pessoas()
    consulta_atividade()
