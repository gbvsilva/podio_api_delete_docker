import json
from get_time import getHour

def handlingPodioError(err):
    hour = getHour()
    message = ""
    if 'x-rate-limit-remaining' in err.status and err.status['x-rate-limit-remaining'] == '0':
        message = f"{hour} -> Quantidade de requisições chegou ao limite por hora."
        print(message)
        return "rate_limit"
    if err.status['status'] == '401':
        # Token expirado. Re-autenticando
        message = f"{hour} -> Token expirado. Renovando..."
        print(message)
        return "token_expired"
    if err.status['status'] == '400':
        if json.loads(err.content)['error_detail'] == 'oauth.client.invalid_secret':
            message = f"{hour} -> Secret inválido."
        elif json.loads(err.content)['error_detail'] == 'user.invalid.username':
            message = f"{hour} -> Usuário inválido."
        elif json.loads(err.content)['error_detail'] == 'oauth.client.invalid_id':
            message = f"{hour} -> ID do cliente inválido."
        elif json.loads(err.content)['error_detail'] == 'user.invalid.password':
            message = f"{hour} -> Senha do cliente inválido."
        else:
            message = f"{hour} -> Parâmetro nulo na query. {err}"
            print(message)
            return "null_query"
        return "status_400"
    if err.status['status'] == '504':
        message = f"{hour} -> Servidor demorou muito para responder. {err}"
        print(message)
        return "status_504"
    else:
        message = f"{hour} -> Erro inesperado no acesso a API. {err}"
    print(message)
    return "not_known_yet"
