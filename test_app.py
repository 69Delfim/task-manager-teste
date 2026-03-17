import pytest
from app import app, init_db
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_home_page(client):
    """Teste Funcional: Verificar se a página inicial carrega"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Minhas Tarefas' in response.data

def test_add_task(client):
    """Teste Funcional: Adicionar uma nova tarefa"""
    response = client.post('/add', data={'title': 'Teste de Qualidade'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Teste de Qualidade' in response.data

def test_empty_task(client):
    """Teste de Validação: Tentar adicionar tarefa vazia"""
    # O sistema atual não valida backend para vazio, o HTML tem 'required'
    # Isso é um ponto de melhoria para o seu relatório!
    response = client.post('/add', data={'title': ''}, follow_redirects=True)
    assert response.status_code == 200