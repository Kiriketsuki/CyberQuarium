import requests

r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'fish called greatwhiteshark',
        'grid_size': '1',
    },
    headers={'api-key': '7ee3371f-03f3-4520-a2d2-6f473f5a5b4e', 'grid_size': "1"}
)
print(r.json()['output_url'])