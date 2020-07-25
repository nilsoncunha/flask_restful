from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
    '''retorna, atualiza e deleta pessoa pelo nome'''

    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {'status': 'error', 'mensagem': f"Pessoa '{nome}' não localizada"}
        return response

    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
            pessoa.save()
        except AttributeError:
            response = {'status': 'error', 'mensagem': f"Pessoa '{nome}' não localizada"}
        return response

    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            response = {'status': 'sucesso', 'mensage': f"Pessoa '{nome}' excluída com sucesso"}
        except AttributeError:
            response = {'status': 'erro', 'mensagem': f"Pessoa '{nome}' não localizada"}
        return response


class ListaInserePessoas(Resource):
    '''insere uma pessoa ou retorna toda a lista da base '''

    def get(self):
        pessoas = Pessoas.query.all()
        if pessoas == []:
            response = {'status': 'erro', 'mensagem': f"Não há pessoa(s) cadastradas"}
        else:
            response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class Atividade(Resource):
    '''retorna, atualiza ou deleta as atividades pelo id'''

    def get(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            response = {
                'id': atividade.id,
                'pessoa': atividade.pessoa.nome,
                'tarefa': atividade.tarefa,
                'status': atividade.status
            }
        except AttributeError:
            response = {'status': 'erro', 'mensagem': f"atividade '{id}' não localizada"}
        return response

    def put(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            dados = request.json
            atividade.status = dados['status']
            response = {
                'id': atividade.id,
                'pessoa': atividade.pessoa.nome,
                'tarefa': atividade.tarefa,
                'status': atividade.status
            }
            atividade.save()
        except AttributeError:
            response = {'status': 'erro', 'mensagem': f"atividade '{id}' não localizada"}
        return response

    def delete(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            mensagem = f'Mensagem {atividade.id} excluida com sucesso'
            response = {'status': 'ok', 'mensagem': mensagem}
        except AttributeError:
            response = {'status': 'error', 'mensagem': f"atividade '{id}' não localizada"}
        return response

class ListaInsereAtividades(Resource):
    '''insere uma atividade ou retorna toda a lista da base '''

    def get(self):
        atividades = Atividades.query.all()
        if atividades == []:
            response = {'status': 'erro', 'mensagem': f"Não há atividade(s) cadastradas"}
        else:
            response = [{'id': i.id, 'tarefa': i.tarefa, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividades]
        return response

    def post(self):
        dados = request.json
        # primeiro pega a pessoa para depois inserir a atividade
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'status': atividade.status
        }
        return response

class AtividadesPessoa(Resource):
    '''retorna as atividades associadas a uma pessoa'''

    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        if pessoa == None:
            response = {'status': 'erro', 'mensagem': f"Atividades para '{nome}' não localizada"}
        else:
            atividades = Atividades.query.filter_by(pessoa=pessoa)
            response = [{'id': i.id, 'pessoa': i.pessoa.nome,
                         'tarefa': i.tarefa, 'status': i.status} for i in atividades]
        return response

class AtividadesStatus(Resource):
    '''retorna as atividades pelo status'''

    def get(self, status):
        atividades = Atividades.query.filter_by(status=status)
        if atividades == None:
            response = {'status': 'erro', 'mensagem': f"status '{status}' não localizado"}
        else:
            response = [{'id': i.id, 'pessoa': i.pessoa.nome,
                         'tarefa': i.tarefa, 'status': i.status} for i in atividades]
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>')  # get, put, delete
api.add_resource(ListaInserePessoas, '/pessoa')  # get, post
api.add_resource(Atividade, '/atividade/<int:id>')  # get, put, delete
api.add_resource(ListaInsereAtividades, '/atividade')  # get, post
api.add_resource(AtividadesPessoa, '/atividade/pessoa/<string:nome>')  # get
api.add_resource(AtividadesStatus, '/atividade/status/<string:status>') # get


if __name__ == '__main__':
    app.run(debug=True)
