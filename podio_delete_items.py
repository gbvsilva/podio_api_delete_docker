from get_time import getHour

from psycopg2 import Error as dbError
from get_mydb import getDB

from pypodio2.transport import TransportException
from podio_tools import handlingPodioError


def deleteItems(podio, apps_ids):
    # Acessando o BD
    mydb = getDB()
    cursor = mydb.cursor()
    for app_id in apps_ids:
        # Criando as tabelas para cada database criado acima
        try:
            appInfo = podio.Application.find(app_id)
            spaceName = podio.Space.find(appInfo.get('space_id')).get('url_label').replace('-', '_')
            appName = appInfo.get('url_label').replace('-', '_')

            tableName = spaceName+"__"+appName

            cursor.execute(f'SELECT id FROM podio.{tableName}')
            itemIDs = cursor.fetchall()
            for id in itemIDs:
                try:
                    podio.Item.find(int(id[0]))
                except TransportException as err:
                    if 'not found' in err.content:
                        print(f'Item ID={id[0]} da tabela "{tableName}" excluído do Podio. Apagando-o do BD...')
                        cursor.execute(f"DELETE FROM podio.{tableName} WHERE id='{id[0]}'")
            
        except dbError as err:
            hour = getHour()
            message = f"{hour} -> Erro no acesso ao BD. {err}"
            print(message)
        except TransportException as err:
            handled = handlingPodioError(err)
            if handled == 'token_expired':
                return 3
            if handled == 'status_400' or handled == 'not_known_yet':
                continue
    mydb.close()
    return 0
