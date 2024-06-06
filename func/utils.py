import os
import json

# Verificação e edição de um usuario.
def session(id, val, type, save, check):
    filename = os.path.join(f"./sessions/{id}.json")
    if not os.path.exists(filename):
        return "not found"
    
    with open(filename, 'r') as file:
        data = json.load(file)
        
    if check:
        if type == 1:
            return data["nome"]
        elif type == 2:
            return data["phone"]
        elif type == 3:
            return data["status"]
        elif type == 4:
            return data["os_active"]
        elif type == 5:
            return data["messages"][0]["os"]
        elif type == 6:
            return data["OSAtendimento"]
        elif type == 7:
            return data["temp"]
        elif type == 8:
            return data["setor"]        
    else:
        if save:
            if type == 1:
                data["nome"] = val
            elif type == 2:
                data["phone"] = val
            elif type == 3:
                data["status"] = val
            elif type == 4:
                data["os_active"] = val
            elif type == 5:
                data["messages"][0]["os"] = val
            elif type == 6:
                data["OSAtendimento"] = val
            elif type == 7:
                data["temp"] = val
            elif type == 8:
                data["setor"] = val
            
            with open(filename, 'w') as file:
                json.dump(data, file)

# Criando json de usuario.
def create_session(chat_id):
    filename = os.path.join(f"./sessions/{chat_id}.json")
    data = {
        "nome": "",
        "phone": "",
        "status": 1,
        "os_active": False,
        "inAtendimento": False,
        "setor": "tecnico",
        "ChatAtendimentoID": 0,
        "OSAtendimento": 0,
        "temp": 0,
        "messages": [
        ]
    }
    with open(filename, 'w') as file:
        json.dump(data, file)

# Verificação e edição de uma OS.
def ordem(id, val, type, save, check):
    filename = os.path.join(f"./os/{id}.json")
    if not os.path.exists(filename):
        return "not found"
    
    with open(filename, 'r') as file:
        data = json.load(file)
        
    if check:
        if type == 1:
            return data["tecid"]
        elif type == 2:
            return data["ateid"]
        elif type == 3:
            return data["process"]            
    else:
        if save:
            if type == 1:
                data["tecid"] = val
            elif type == 2:
                data["ateid"] = val
            elif type == 3:
                data["process"] = val
            
            with open(filename, 'w') as file:
                json.dump(data, file)

# Criando json de ums OS.
def create_ordem(os_id, tecid):
    filename = os.path.join(f"./os/{os_id}.json")
    data = {
        "tecid": tecid,
        "ateid": "",
        "process": 0,
    }
    with open(filename, 'w') as file:
        json.dump(data, file)

# Coletar todos usuarios do setor noc.
def get_ids_with_noc_sector(directory="./sessions/"):
    noc_ids = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                if data.get("setor") == "noc" and data.get("OSAtendimento") == 0:
                    noc_ids.append(filename.split('.')[0])
    return noc_ids

# Coletar todos os ids de OS do usuario.
def get_ids_my_os(id, directory="./os/"):
    os_ids = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                if data.get("tecid") == id:
                    os_ids.append(filename.split('.')[0])
    return os_ids

# Coletar todos os ids de OS abertas.
def get_ids_with_os(directory="./os/"):
    os_ids = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                if data.get("process") == 0:
                    os_ids.append(filename.split('.')[0])
    return os_ids