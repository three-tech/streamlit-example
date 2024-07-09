import base64

import requests

# 设置consul的地址和token
from_consul_url = "http://10.0.0.20:8500"
to_consul_url = "http://10.0.0.21:8500"
exclude_keys = ["config/application/application"]
token = "your_consul_token"

# 设置本地存储数据的字典
local_data = {}
sync_flag = {}


# 从consul获取kv store中的数据
def get_data_from_consul():
    global local_data
    response = requests.get(f"{from_consul_url}/v1/kv/?recurse", headers={"X-Consul-Auth": token})
    if response.status_code == 200:
        for data in response.json():
            if data['Key'] in exclude_keys or data['Value'] is None:
                print(f"Skip key: {data['Key']}")
                continue
            if data['Key'] in local_data and local_data[data['Key']] == base64.b64decode(data['Value']):
                print(f"not changed key: {data['Key']}")
                sync_flag[data['Key']] = True
                continue
            local_data[data['Key']] = base64.b64decode(data['Value'])
            sync_flag[data['Key']] = False
    else:
        print("Failed to get data from consul:" + response.text)


# 将数据同步到consul的kv store
def sync_data_to_consul():
    headers = {"X-Consul-Auth": token, 'Content-Type': 'text/plain'}
    for key, value in local_data.items():
        if sync_flag[key]:
            print(f"Not changed data,Skip sync key: {key}")
            continue
        response = requests.put(f"{to_consul_url}/v1/kv/{key}", headers=headers, data=value)
        if response.status_code != 200:
            print(f"Failed to sync data to consul for key: {key}")
        else:
            print(f"Sync data to consul for key: {key}")


# 监听本地数据的变化，实时同步到consul
def sync_data():
    try:
        get_data_from_consul()
        sync_data_to_consul()
    except Exception as e:
        print("Failed to sync data", e)
        pass


# 运行数据同步
sync_data()
