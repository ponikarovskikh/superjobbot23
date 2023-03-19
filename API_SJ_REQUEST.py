import requests
import json
import  time




def savetoken():
   with open('tokens.json', 'r') as f:
      dict = json.load(f)
   return (dict['access_token'])


def get_new_api_key():
    with open('tokens.json', 'r') as f:
        dict = json.load(f)
    params = {
        "refresh_token": dict["refresh_token"],
        "client_id": '2100',
        "client_secret": dict['client_secret']
    }

    url = "https://api.superjob.ru/2.0/oauth2/refresh_token/"
    response = requests.get(url, params=params)
    resjson = response.json()
    acc = resjson['access_token']
    with open('tokens.json', 'r') as f:
        dict = json.load(f)
    dict['access_token']=acc
    with open('tokens.json', 'w') as f:
        json.dump(dict, f)
    return  acc



def getinfo(keyword, town, payment):
        # идентификация
        # ======================================================
        with open('tokens.json', 'r') as f:
            dict = json.load(f)
        api_key=dict['access_token']
        app_id=dict['client_secret']

        # --------------------------------------------------------
        params = {
            'payment_from': f'{payment}',
            "sort_new": time.time(),
            "keyword": f"{keyword}",
            "town": f'{town}'
        }
        headers = {
            'X-Api-App-Id': app_id,
            'Authorization': f"Bearer {api_key}"
        }
        url = "https://api.superjob.ru/2.0/vacancies/"
        response = requests.get(url, headers=headers, params=params ).json()
        resjson_form = json.dumps(response, ensure_ascii=False, indent=2)
        # ===========================================================
        if 'error' in resjson_form:
            if response['error']['code'] == 410:  # обработка ошибки 410
                new_api_key = get_new_api_key(app_id)  # функция для получения нового ключа
                api_key = new_api_key
                response = requests.get(url, headers={'Authorization': f"Bearer {api_key}",'X-Api-App-Id': app_id},params=params).json()
                resjson_form = json.dumps(response, ensure_ascii=False, indent=2)
                pyform = json.loads(resjson_form)
                newvacancy = pyform['objects']
                return newvacancy

        elif 'objects' in resjson_form:
            pyform = json.loads(resjson_form)
            newvacancy=pyform['objects']
            return newvacancy




































