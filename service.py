from linkedin_api import Linkedin
from config import USER, PASSWORD


class Service:
    def __init__(self):
        self.api = Linkedin(USER, PASSWORD)

    def get_profile(self, data):
        try:
            # Extrair o profile_id da url de perfil
            profile_id = self.extract_profile_id(data)

            # Autenticar e buscar o perfil de acordo com o ID do perfil
            profile = self.api.get_profile(profile_id)
            contact_info = self.api.get_profile_contact_info(profile_id)

            # Criar o perfil formatado
            profile_data = self.format_profile(profile, contact_info)
            print(profile_data)
            return profile_data

        except Exception as e:
            print(f"Erro ao obter o perfil: {e}")
            return {'erro': str(e)}

    # função responsável por extrar o ID da URL do perfil do usuário
    def extract_profile_id(self, url):
        start_index = url.find('/in/') + len('/in/')
        end_index = url.find('/', start_index)
        if end_index == -1:
            end_index = None
        return url[start_index:end_index]

    # função responsável por organizar os dados brutos do perfil do usuário do linkedin em um formato padronizado
    def format_profile(self, profile, contact_info):
        nome = f"{profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}"
        experiencia = profile.get('experience', [{}])[0]
        organizacao = experiencia.get('companyName', 'N/A')
        funcao = experiencia.get('title', 'N/A')
        email = contact_info.get('email_address', 'N/A')
        celular = contact_info.get('phone_numbers', [{}])[0].get('number', 'N/A')
        linkedin = f"www.linkedin.com/in/{profile.get('public_id', '')}"
        cidade = profile.get('geoLocationName', 'N/A').split(',')[0].strip() if profile.get(
            'geoLocationName') else 'N/A'
        estado = profile.get('geoLocationName', 'N/A').split(',')[1].strip() if ',' in profile.get('geoLocationName','') else 'N/A'
        return {
            'nome': nome,
            'organizacao': organizacao,
            'funcao': funcao,
            'email': email,
            'celular': celular,
            'linkedin': linkedin,
            'cidade': cidade,
            'estado': estado
        }
