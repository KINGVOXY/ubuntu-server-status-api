# ubuntu-server-status-api
Ubuntu鯖の状態監視用API

```
.
├── README.md
├── requirements.txt
├── server.py
└── system_example.service
```

## 環境
- Ubuntu 20.04.3 LTS
- sysstat
- Python 3.9.5
- pip 21.1.1 
  - uvicorn 0.18.2
  - fastapi 0.79.0
  - psutil 5.9.1

## 使い方
```sh
python server.py
```

常駐化するときは，[system_sxample.service](./system_sxample.service) を適宜書き換え、`/etc/systemd/system/`下に配置し，

```sh
# 有効化
systemctl enable system_example.service
# 開始
systemctl start system_example.service
```

[localhost:8200/spi/server/status](http://localhost:8200/spi/server/status) にGETすると，Jsonで返ってくる．

## Json
下記の値は一例．

```json
{
	"sysname": "Linux",
	"release": "5.4.0-90-generic",
	"machine": "x86_64",
	"numOfCpus": "4",
	"ioReads": {
		"rtps": "0.0",
		"bread": "0.0"
	},
	"ioWrites": {
		"wtps": "1.48",
		"bwrtn": "29.2"
	},
	"loadavg1": "0.36",
	"loadavg5": "0.22",
	"loadavg15": "0.14",
	"cpuPercent": "2.3",
	"cpuTemperature": "87.0",
	"memoryPercent": "77.2",
	"swapFree": "1522589696",
	"diskPercent": "19.2",
	"interfaces": [
		{
			"name": "lo",
			"bytesSent": "980051737",
			"bytesRecv": "980051737",
			"packetsSent": "4298434",
			"packetsRecv": "4298434",
			"rxkb": "4.72",
			"txkb": "4.72"
		},
		{
			"name": "wlp9s0",
			"bytesSent": "1625189010",
			"bytesRecv": "18039430484",
			"packetsSent": "5844745",
			"packetsRecv": "51048234",
			"rxkb": "2.18",
			"txkb": "4.85"
		},
		{
			"name": "enp4s0",
			"bytesSent": "0",
			"bytesRecv": "0",
			"packetsSent": "0",
			"packetsRecv": "0",
			"rxkb": "0.0",
			"txkb": "0.0"
		}
	]
}
```
