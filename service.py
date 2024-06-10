from linkedin_api import Linkedin
from config import USER, PASSWORD


class Service:
    def __init__(self):
        # Inicializa a instância da API do LinkedIn com as credenciais fornecidas
        self.api = Linkedin(USER, PASSWORD)

    # Função responsável por obter o perfil do LinkedIn com base nos dados fornecidos
    def get_profile(self, data):
        try:
            # Inicializa uma lista vazia que armazenará os textos simples dos links do LinkedIn
            linkedin_plain_texts = []

            # Iterando sobre cada entrada no array 'data'
            for entry in data:
                # Obtem o dicionario 'properties_value' da entrada atual
                # Se properties_value não estiver presente, retorna um dicionário vazio
                properties_value = entry.get("properties_value", {})

                # Obtém uma lista associada a chave 'LinkedIn' dentro de 'properties_value'
                # Se 'LinkedIn' não estiver presente, retorna uma lista vazia.
                linkedin_property = properties_value.get("LinkedIn", [])

                # Itera sobre cada item na lista 'LinkedIn'
                for linkedin in linkedin_property:
                    # Verifica se o item atual contém a chave 'plain_text'
                    if "plain_text" in linkedin:
                        # Adiciona o valor associado à chave 'plain_text' à lista 'linkedin_plain_texts'
                        linkedin_plain_texts.append(linkedin["plain_text"])
            print(linkedin_plain_texts)

            # Extrai os IDs de perfil a partir das URLs de perfil do LinkedIn
            profile_id = self.extract_profile_id(linkedin_plain_texts)
            print(profile_id)

            # Inicializa listas vazias para armazenar perfis e informações de contato
            profile_ = []
            contati_ = []

            # Itera sobre cada ID de perfil
            for id in profile_id:
                # Autenticar e buscar o perfil e informações de contato de acordo com o ID do perfil
                profile = self.api.get_profile(id)
                contact_info = self.api.get_profile_contact_info(id)

                # Adiciona o perfil e as informações de contato às listas correspondentes
                profile_.append(profile)
                contati_.append(contact_info)

            # Formata os dados do perfil
            profile_data = self.format_profile(profile_, contati_)
            print(profile_data)

            # Extrai os IDs dos dados de entrada
            ids = [item["id"] for item in data]

            # Adiciona um ID a cada objeto no perfil formatado
            for i, item in enumerate(profile_data):
                item["id"] = ids[i]

            # Retorna os dados do perfil formatado
            return profile_data

        # Captura e imprime qualquer exceção que ocorra, retornando uma mensagem de erro
        except Exception as e:
            print(f"Erro ao obter o perfil: {e}")
            return {'erro': str(e)}

    # Função responsável por extrar o ID da URL do perfil do usuário
    def extract_profile_id(self, urls):
        profile_ids = []

        # Itera sobre cada URL fornecida
        for url in urls:
            # Encontra o índice inicial do ID do perfil na URL
            start_index = url.find('/in/') + len('/in/')
            # Encontra o índice final do ID do perfil na URL
            end_index = url.find('/', start_index)
            if end_index == -1:
                end_index = None
            # Adiciona o ID do perfil à lista de IDs
            profile_ids.append(url[start_index:end_index])
        return profile_ids

    # Função responsável por organizar os dados brutos do perfil do usuário do linkedin em um formato padronizado
    def format_profile(self, profile, contact):
        print("PROFILE ", profile)

        # Inicializa uma lista vazia para armazenar os objetos formatados
        obje = []

        # Itera sobre cada objeto de perfil
        for obj in profile:
            nome = f"{obj.get('firstName')} {obj.get('lastName')}"
            experiencia = obj.get('experience', [{}])[0]
            organizacao = experiencia.get('companyName')
            funcao = experiencia.get('title')
            linkedin = f"www.linkedin.com/in/{obj.get('public_id', '')}"
            cidade = obj.get('geoLocationName', 'N/A').split(',')[0].strip() if obj.get(
                'geoLocationName') else 'N/A'
            estado = obj.get('geoLocationName', 'N/A').split(',')[1].strip() if ',' in obj.get('geoLocationName',
                                                                                               '') else 'N/A'
            email = contact[0].get('email_address', 'N/A')
            telefone = contact[0].get('phone_numbers', [{}])[0].get('number', 'N/A')

            # Adiciona as informações à lista de objetos
            obje.append(nome)
            obje.append(experiencia)
            obje.append(organizacao)
            obje.append(funcao)
            obje.append(linkedin)
            obje.append(cidade)
            obje.append(estado)
            obje.append(email)
            obje.append(telefone)

            print("DADO FINAL ", obje)
            # Cria um dicionário formatado com as informações do perfil
            perfil = {
                'nome': nome,
                'organizacao': organizacao,
                'funcao': funcao,
                'linkedin': linkedin,
                'cidade': cidade,
                'estado': estado,
                'email': email,
                'telefone': telefone
            }

            # Adiciona o dicionário formatado à lista de objetos
            obje.append(perfil)

        # Define as chaves desejadas para os objetos filtrados
        chaves_desejadas = {"cidade", "email", "estado", "funcao", "linkedin", "nome", "organizacao"}

        """
        Aqui, é feita uma compreensão de lista para filtrar os objetos contidos em obje. Cada objeto é verificado 
        para garantir que seja um dicionário (isinstance(obj, dict)) e que contenha todas as chaves desejadas 
        (chaves_desejadas.issubset(obj.keys())). Se todas as chaves desejadas estiverem presentes no dicionário, o 
        objeto é incluído na lista objetos_filtrados.
        """
        objetos_filtrados = [obj for obj in obje if isinstance(obj, dict) and chaves_desejadas.issubset(obj.keys())]
        for obj in objetos_filtrados:
            print(obj)

        return objetos_filtrados
