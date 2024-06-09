from linkedin_api import Linkedin
from config import USER, PASSWORD


class Service:
    def __init__(self):
        self.api = Linkedin(USER, PASSWORD)

    def get_profile(self, data):
        try:
            linkedin_plain_texts = []

            for entry in data:
                properties_value = entry.get("properties_value", {})
                linkedin_property = properties_value.get("LinkedIn", [])
                for linkedin in linkedin_property:
                    if "plain_text" in linkedin:
                        linkedin_plain_texts.append(linkedin["plain_text"])
            print(linkedin_plain_texts)

            # Extrair o profile_id da url de perfil
            profile_id = self.extract_profile_id(linkedin_plain_texts)
            print(profile_id)

            profile_ = []
            contati_ = []

            for id in profile_id:
                # Autenticar e buscar o perfil de acordo com o ID do perfil
                profile = self.api.get_profile(id)
                contact_info = self.api.get_profile_contact_info(id)

                profile_.append(profile)
                contati_.append(contact_info)

            # Criar o perfil formatado
            profile_data = self.format_profile(profile_, contati_)
            print(profile_data)

            ids = [item["id"] for item in data]
            # Adicionando um ID a cada objeto
            for i, item in enumerate(profile_data):
                item["id"] = ids[i]

            return profile_data

        except Exception as e:
            print(f"Erro ao obter o perfil: {e}")
            return {'erro': str(e)}

    # função responsável por extrar o ID da URL do perfil do usuário
    def extract_profile_id(self, urls):
        profile_ids = []

        for url in urls:
            start_index = url.find('/in/') + len('/in/')
            end_index = url.find('/', start_index)
            if end_index == -1:
                end_index = None
            profile_ids.append(url[start_index:end_index])
        return profile_ids

    # função responsável por organizar os dados brutos do perfil do usuário do linkedin em um formato padronizado
    def format_profile(self, profile, contact):
        print("PROFILE ", profile)

        obje = []
        for obj in profile:
            nome = f"{obj.get('firstName')} {obj.get('lastName')}"
            experiencia = obj.get('experience', [{}])[0]
            organizacao = experiencia.get('companyName')
            funcao = experiencia.get('title')
            email = contact[0].get('email_address', 'N/A')
            #celular = contact.get('phone_numbers', [{}])[0].get('number', 'N/A')
            linkedin = f"www.linkedin.com/in/{obj.get('public_id', '')}"
            cidade = obj.get('geoLocationName', 'N/A').split(',')[0].strip() if obj.get(
                'geoLocationName') else 'N/A'
            estado = obj.get('geoLocationName', 'N/A').split(',')[1].strip() if ',' in obj.get('geoLocationName','') else 'N/A'

            obje.append(nome)
            obje.append(experiencia)
            obje.append(organizacao)
            obje.append(funcao)
            obje.append(linkedin)
            obje.append(cidade)
            obje.append(estado)
            obje.append(email)

            print("DADO FINAL ", obje)
            perfil = {
                'nome': nome,
                'organizacao': organizacao,
                'funcao': funcao,
                'linkedin': linkedin,
                'cidade': cidade,
                'estado': estado,
                'email': email
            }

            obje.append(perfil)

        chaves_desejadas = {"cidade", "email", "estado", "funcao", "linkedin", "nome", "organizacao"}
        objetos_filtrados = [obj for obj in obje if isinstance(obj, dict) and chaves_desejadas.issubset(obj.keys())]
        for obj in objetos_filtrados:
            print(obj)

        return objetos_filtrados