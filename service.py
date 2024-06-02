from linkedin_api import Linkedin
from config import USER, PASSWORD
from app import app


class Service:
    def get_profile(self, data):
        # Authenticate using any Linkedin account credentials

        # Encontrar a posição de /in/
        start_index = data.find('/in/') + len('/in/')

        # Extrair tudo após /in/
        result = data[start_index:]

        # Remover a barra final, se houver
        if result.endswith('/'):
            profile_id = result[:-1]

        api = Linkedin(USER, PASSWORD)
        print(profile_id)
        # GET a profile
        profile = api.get_profile(profile_id)
        contact_info = api.get_profile_contact_info(profile_id)
        print(profile)

        nome = profile['firstName'] + " " + profile['lastName']
        organizacao = profile['experience'][0]['companyName']
        funcao = profile['experience'][0]['title']
        email = contact_info['email_address']
        if contact_info['phone_numbers']:
            celular = contact_info['phone_numbers'][0]['number']
        else:
            celular = "N/A."


        linkedin = 'www.linkedin.com/in/' + profile['public_id']
        cidade = profile['geoLocationName'].split(',')[0].strip()
        estado = profile['geoLocationName'].split(',')[1].strip()

        print(nome, organizacao, funcao, email, celular, linkedin, cidade, estado)
        cargo = ""
        indicacoes = ""
        profile_data = {
            'nome': nome,
            'organizacao': organizacao,
            'funcao': funcao,
            'email': email,
            'celular': celular,
            'linkedin': linkedin,
            'cidade': cidade,
            'estado': estado

        }

        return profile_data

        # GET a profiles contact info

        print("Informações de contatos:", contact_info)
        """
        # GET 1st degree connections of a given profile
        connections = api.get_profile_connections('1234asc12304')"""
