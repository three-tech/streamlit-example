import base64

import requests

# 设置consul的地址和token
from_consul_url = "http://10.0.0.19:8500"
to_consul_url = "http://localhost:8500"
exclude_keys = ["config/application/application"]
token = "your_consul_token"

# 设置本地存储数据的字典
local_data = {}


# 从consul获取kv store中的数据
def get_data_from_consul():
    global local_data
    response = requests.get(f"{from_consul_url}/v1/kv/?recurse", headers={"X-Consul-Auth": token})
    if response.status_code == 200:
        for data in response.json():
            if data['Key'] in exclude_keys or data['Value'] is None:
                print(f"Skip key: {data['Key']}")
                continue
            local_data[data['Key']] = base64.b64decode(data['Value']).decode("utf-8")
    else:
        print("Failed to get data from consul:" + response.text)


# 将数据同步到consul的kv store
def sync_data_to_consul():
    headers = {"X-Consul-Auth": token, 'Content-Type': 'text/plain'}
    for key, value in local_data.items():
        # response = requests.put(f"{to_consul_url}/v1/kv/{key}", headers=headers, data=value)
        # 使用 files 参数传递数据
        files = {"file": ("data.txt", value)}
        response = requests.put(f"{to_consul_url}/v1/kv/{key}", headers=headers, data=value.encode('utf-8'))
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
        print("Failed to sync data")
        pass


# 运行数据同步
sync_data()
