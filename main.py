from os import environ as env
# Usando a biblioteca de manipulação da API do Podio.
from pypodio2 import api
from pypodio2.transport import TransportException

import time

from get_time import getHour, timer
from podio_delete_items import deleteItems
from podio_tools import handlingPodioError

if __name__ == '__main__':
    # Período de atualização do banco
    timeOffset = int(env.get('TIMEOFFSET'))

    # Recuperando as variáveis de ambiente e guardando
    client_id = env.get('PODIO_CLIENT_ID')
    client_secret = env.get('PODIO_CLIENT_SECRET')
    username = env.get('PODIO_USERNAME')
    password = env.get('PODIO_PASSWORD')
    # Apps IDs
    apps_ids = list(map(int, env.get('PODIO_APPS_IDS').split(',')))

    message = "==== PODIO API DELETE SCRIPT (PostgreSQL) ===="
    print(message)
   
    # Autenticando na plataforma do Podio com as credenciais recuperadas acima
    try:
        podio = api.OAuthClient(
            client_id,
            client_secret,
            username,
            password
        )
    # Caso haja erro, provavelmente o token de acesso a API expirou.
    except TransportException as err:
        hour = getHour()
        handled = handlingPodioError(err)
        if handled == 'status_400':
            message = "Terminando o programa."
            print(message)
        exit(1)
    else:
        cycle = 1
        while True:
            message = f"==== Ciclo {cycle} ===="
            print(message)
            deletion = deleteItems(podio, apps_ids)
            if deletion == 0:
                hours = getHour(seconds=timeOffset)
                message = f"Esperando as próximas {timeOffset/3600}hs. Até às {hours}"
                timer(timeOffset)
            elif deletion == 2:
                hour = getHour(hours=1)
                message = f"Esperando a hora seguinte às {hour}"
                print(message)
                timer(3600)
                podio = api.OAuthClient(	
                    client_id,	
                    client_secret,	
                    username,	
                    password	
                )
            elif deletion == 3:
                message = "Tentando novamente..."
                print(message)
                podio = api.OAuthClient(	
                    client_id,	
                    client_secret,	
                    username,	
                    password	
                )
                time.sleep(1)
            else:
                hour = getHour()
                message = f"{hour} -> Erro inesperado na criação/atualização do BD. Terminando o programa."
                print(message)
                exit(1)
            cycle += 1
