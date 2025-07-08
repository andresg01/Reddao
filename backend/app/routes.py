# backend/app/routes.py

from flask import request, jsonify, current_app as app
from . import blockchain, db, node_identifier
import math

# --- LÓGICA DE GOBERNANZA ---
def get_voting_power(wallet_id):
    """
    Calcula el poder de voto según el tipo de stakeholder.
    """
    for user, data in db['users'].items():
        if data['wallet_id'] == wallet_id:
            user_type = data['user_type']
            if user_type == 'user': return 50
            if user_type == 'investor': return 30
            if user_type == 'employee': return 10
            if user_type == 'provider': return 10
            if user_type == 'center_admin': return 30
    return 0

# --- RUTAS DE LA API ---

@app.route('/')
def index():
    return "Servidor REDDAO Backend funcionando!"

@app.route('/api/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1, transaction_type="mining_reward")
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    return jsonify({'message': "Nuevo bloque minado", 'block': block}), 200

@app.route('/api/transactions/new', methods=['POST'])
def new_transaction_api():
    """
    Gestiona todo tipo de transacciones, diferenciando su lógica.
    """
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'transaction_type']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sender_wallet = db['wallets'].get(values['sender'])
    transaction_type = values['transaction_type']

    # Solo se comprueban los fondos si la transacción implica un gasto (cantidad > 0)
    if values['amount'] > 0 and (not sender_wallet or sender_wallet['balance'] < values['amount']):
        return 'Insufficient funds', 400

    # --- LÓGICA DIFERENCIADA POR TIPO DE TRANSACCIÓN ---

    if transaction_type == 'pago_servicio':
        center_wallet_id = values['recipient']
        amount = values['amount']
        db['wallets'][center_wallet_id]['balance'] += amount * 0.65
        db['wallets']['reddao_business_wallet']['balance'] += amount * 0.25
        db['wallets']['reddao_marketing_wallet']['balance'] += amount * 0.10
        db['wallets'][values['sender']]['balance'] -= amount
        blockchain.new_transaction(values['sender'], center_wallet_id, amount * 0.65, 'distribucion_servicio', values.get('details', {}))
        blockchain.new_transaction(values['sender'], 'reddao_business_wallet', amount * 0.25, 'distribucion_servicio', values.get('details', {}))
        blockchain.new_transaction(values['sender'], 'reddao_marketing_wallet', amount * 0.10, 'distribucion_servicio', values.get('details', {}))
        return jsonify({'message': 'Pago procesado y distribuido.'}), 201

    elif transaction_type in ['vote', 'create_proposal']:
        # Estas acciones no mueven dinero, solo se registran.
        # CORRECCIÓN: Se procesan aquí para que no intenten modificar balances.
        details = values.get('details', {})
        
        # Si es un voto, actualizamos la propuesta
        if transaction_type == 'vote' and 'proposal_id' in details:
            proposal_id = details['proposal_id']
            voter_wallet = details['voter_wallet']
            
            if proposal_id in db['proposals'] and voter_wallet not in db['proposals'][proposal_id]['voters']:
                power = get_voting_power(voter_wallet)
                db['proposals'][proposal_id]['votes'][details['vote']] += power
                db['proposals'][proposal_id]['voters'].append(voter_wallet)

        # Si es una nueva propuesta, la añadimos a la base de datos
        elif transaction_type == 'create_proposal' and 'title' in details:
            proposal_id = f"prop_{len(db['proposals']) + 1}"
            db['proposals'][proposal_id] = {
                'id': proposal_id, 'title': details['title'], 'description': details.get('description', ''),
                'creator': values['sender'], 'status': 'active',
                'votes': {"yes": 0, "no": 0}, 'voters': []
            }
            details['proposal_id'] = proposal_id # Añadimos el nuevo ID a los detalles de la transacción

        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            transaction_type, details
        )
        return jsonify({'message': f'Acción de gobernanza registrada en el bloque {index}'}), 201

    else: # Para todas las demás transacciones simples (propinas, compras)
        db['wallets'][values['sender']]['balance'] -= values['amount']
        db['wallets'][values['recipient']]['balance'] += values['amount']
        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            transaction_type, values.get('details', {})
        )
        return jsonify({'message': f'Transacción simple añadida al bloque {index}'}), 201


@app.route('/api/proposals/<proposal_id>/vote', methods=['POST'])
def vote_on_proposal(proposal_id):
    # Esta ruta ahora es redundante, ya que la lógica se ha movido a /transactions/new
    # La mantenemos por compatibilidad pero idealmente se refactorizaría el frontend para no usarla.
    values = request.get_json()
    required = ['voter_wallet', 'vote']
    if not all(k in values for k in required) or proposal_id not in db['proposals']:
        return 'Missing values or invalid proposal', 400
    
    proposal = db['proposals'][proposal_id]
    if values['voter_wallet'] in proposal['voters']:
        return 'Voter has already voted', 400

    power = get_voting_power(values['voter_wallet'])
    proposal['votes'][values['vote']] += power
    proposal['voters'].append(values['voter_wallet'])
    
    return jsonify({'message': 'Vote registered (legacy)', 'proposal': proposal}), 200

@app.route('/api/proposals', methods=['POST'])
def create_proposal():
    # Esta ruta ahora es redundante, la lógica está en /transactions/new
    values = request.get_json()
    required = ['creator_wallet', 'title', 'description']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    proposal_id = f"prop_{len(db['proposals']) + 1}"
    db['proposals'][proposal_id] = {
        'id': proposal_id, 'title': values['title'], 'description': values['description'],
        'creator': values['creator_wallet'], 'status': 'active',
        'votes': {"yes": 0, "no": 0}, 'voters': []
    }
    return jsonify({'message': 'Proposal created (legacy)', 'proposal': db['proposals'][proposal_id]}), 201

# El resto de las rutas (data/all, chain, etc.) no necesitan cambios.
@app.route('/api/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/api/data/all', methods=['GET'])
def get_all_data():
    return jsonify(db)
