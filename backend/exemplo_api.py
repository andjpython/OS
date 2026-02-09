"""
Script de exemplo para testar a API REST do sistema de OS.
Execute o servidor primeiro: python manage.py runserver
"""

import requests
from datetime import datetime

BASE_URL = 'http://localhost:8000/api'


def exemplo_fluxo_completo():
    """Demonstra um fluxo completo de uso da API"""
    
    print("=" * 60)
    print("EXEMPLO DE FLUXO COMPLETO - SISTEMA DE OS")
    print("=" * 60)
    
    # 1. Criar status
    print("\n1. Criando status...")
    status_aberta = criar_status("Aberta", "OS em aberto")
    status_finalizada = criar_status("Finalizada", "OS concluída")
    print(f"   ✓ Status criados: {status_aberta['id']}, {status_finalizada['id']}")
    
    # 2. Criar profissionais
    print("\n2. Criando profissionais...")
    prof1 = criar_profissional("João Silva", "1234")
    prof2 = criar_profissional("Maria Santos", "5678")
    print(f"   ✓ Profissionais criados: {prof1['nome']}, {prof2['nome']}")
    
    # 3. Criar ordem de serviço
    print("\n3. Criando ordem de serviço...")
    os = criar_ordem_servico(
        numero="OS-2026-001",
        descricao="Instalação de equipamento na sala 10",
        status_id=status_aberta['id'],
        profissionais_ids=[prof1['id'], prof2['id']]
    )
    print(f"   ✓ OS criada: {os['numero']}")
    
    # 4. Listar ordens de serviço
    print("\n4. Listando ordens de serviço...")
    ordens = listar_ordens()
    print(f"   ✓ Total de OSs: {len(ordens)}")
    
    # 5. Criar ação técnica
    print("\n5. Criando ação técnica...")
    acao = criar_acao_tecnica(
        os['id'],
        prof1['id'],
        "Instalação do equipamento realizada com sucesso"
    )
    print(f"   ✓ Ação criada: ID {acao['id']}")
    
    # 6. Finalizar OS
    print("\n6. Finalizando ordem de serviço...")
    os_finalizada = finalizar_ordem(os['id'], status_finalizada['id'])
    print(f"   ✓ OS finalizada em: {os_finalizada['data_finalizacao']}")
    print(f"   ✓ Tempo total: {os_finalizada['tempo_total_minutos']} minutos")
    
    # 7. Buscar profissional por matrícula
    print("\n7. Buscando profissional por matrícula...")
    resultado = buscar_profissional_por_matricula("1234")
    print(f"   ✓ Encontrado: {resultado[0]['nome']}")
    
    print("\n" + "=" * 60)
    print("FLUXO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)


def criar_status(nome, descricao):
    """Cria um status de OS (via admin ou shell)"""
    # Nota: Status normalmente são criados via admin
    return {'id': 1, 'nome': nome, 'descricao': descricao}


def criar_profissional(nome, matricula):
    """Cria um profissional"""
    response = requests.post(
        f'{BASE_URL}/profissionais/',
        json={'nome': nome, 'matricula': matricula, 'ativo': True}
    )
    return response.json()


def criar_ordem_servico(numero, descricao, status_id, profissionais_ids):
    """Cria uma ordem de serviço"""
    response = requests.post(
        f'{BASE_URL}/ordens/',
        json={
            'numero': numero,
            'descricao': descricao,
            'status': status_id,
            'profissionais': profissionais_ids
        }
    )
    return response.json()


def listar_ordens(status_id=None, profissional_id=None):
    """Lista ordens de serviço com filtros opcionais"""
    params = {}
    if status_id:
        params['status_id'] = status_id
    if profissional_id:
        params['profissional_id'] = profissional_id
    
    response = requests.get(f'{BASE_URL}/ordens/', params=params)
    return response.json()


def criar_acao_tecnica(ordem_id, profissional_id, descricao):
    """Cria uma ação técnica"""
    response = requests.post(
        f'{BASE_URL}/acoes/',
        json={
            'ordem_servico': ordem_id,
            'profissional': profissional_id,
            'descricao': descricao
        }
    )
    return response.json()


def finalizar_ordem(ordem_id, status_id=None):
    """Finaliza uma ordem de serviço"""
    data = {}
    if status_id:
        data['status_id'] = status_id
    
    response = requests.post(
        f'{BASE_URL}/ordens/{ordem_id}/finalizar/',
        json=data
    )
    return response.json()


def buscar_profissional_por_matricula(matricula):
    """Busca profissional por matrícula"""
    response = requests.get(
        f'{BASE_URL}/profissionais/',
        params={'matricula': matricula}
    )
    return response.json()


if __name__ == '__main__':
    print("\n⚠️  ATENÇÃO: Certifique-se de que o servidor está rodando!")
    print("Execute: python manage.py runserver\n")
    
    try:
        exemplo_fluxo_completo()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o Django está rodando em http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
