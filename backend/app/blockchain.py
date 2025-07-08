import hashlib
import json
from time import time

class Blockchain:
    """
    Clase que gestiona la cadena de bloques, transacciones y nodos.
    """
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Crear el bloque génesis
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Crea un nuevo bloque y lo añade a la cadena.
        :param proof: <int> La prueba de trabajo.
        :param previous_hash: (Opcional) <str> Hash del bloque anterior.
        :return: <dict> Nuevo bloque.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Resetear la lista de transacciones pendientes
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, transaction_type, details={}):
        """
        Añade una nueva transacción a la lista de transacciones pendientes.
        :param sender: <str> Dirección del remitente.
        :param recipient: <str> Dirección del destinatario.
        :param amount: <float> Cantidad.
        :param transaction_type: <str> Tipo de transacción.
        :param details: <dict> Detalles adicionales.
        :return: <int> El índice del bloque que contendrá esta transacción.
        """
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'transaction_type': transaction_type,
            'details': details,
            'timestamp': time()
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        """Devuelve el último bloque de la cadena."""
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Hashea un bloque usando SHA-256.
        :param block: <dict> Bloque.
        :return: <str> Hash.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Algoritmo de Prueba de Trabajo simple.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Valida la prueba: ¿El hash(last_proof, proof) contiene 4 ceros al principio?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
