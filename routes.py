from flask import request, jsonify
from service import Service
from app import app

service = Service()


@app.route('/profileUrl', methods=['POST'])
def profile_url():
    try:
        # Verifica se o JSON recebido contém a chave 'data'
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'Invalid input, "data" key is missing'}), 400

        data_str = data['data']
        print(data_str)
        # chamar o serviço para obter os dados do perfil
        profile_data = service.get_profile(data_str)

        # Verifique se o profile_data contém um erro
        if 'erro' in profile_data:
            return jsonify({'error': profile_data['erro']}), 500

        return jsonify(profile_data), 200
    except Exception as e:
        # Log do erro
        app.logger.error(f"Erro ao processar a solicitação: {e}")
        return jsonify({'error': 'Internal server error'}), 500
