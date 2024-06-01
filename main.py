from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('', '')

# GET a profile
profile = api.get_profile('thulio-freires')
contact_info = api.get_profile_contact_info('thulio-freires')
print(profile)

nome = profile['firstName'] + profile['lastName']
organizacao = profile['experience'][0]['companyName']
funcao = profile['experience'][0]['title']
email = contact_info['email_address']
celular = contact_info['phone_numbers'][0]['number']
linkedin = 'www.linkedin.com/in/', profile['public_id']
cidade = profile['geoLocationName'].split(',')[0].strip()
estado = profile['geoLocationName'].split(',')[1].strip()

print(nome, organizacao, funcao, email, celular, linkedin, cidade, estado)
cargo = ""
indicacoes = ""

# GET a profiles contact info

print("Informações de contatos:", contact_info)
"""
# GET 1st degree connections of a given profile
connections = api.get_profile_connections('1234asc12304')"""