# 一个非常简单的Demo，演示如何使用 Serverless Framework来部署 AWS API Gateway + Lambda


### 安装

Serverless Framework提供了一个CLI工具（基于Node.js）, 在本机安装好Node.js后，通过如下命令可安装Serverless Framework:

```console
$ npm install -g serverless
```

### 初始化项目

通过如下命令创建一个基于python3模板的项目：

```bash
$ sls create --template aws-python3 --path sls-lambda-python3 
Serverless: Generating boilerplate...
Serverless: Generating boilerplate in "/Users/linjungz/projects/sandbox/sls-lambda-demo/sls-lambda-python3"
 _______                             __
|   _   .-----.----.--.--.-----.----|  .-----.-----.-----.
|   |___|  -__|   _|  |  |  -__|   _|  |  -__|__ --|__ --|
|____   |_____|__|  \___/|_____|__| |__|_____|_____|_____|
|   |   |             The Serverless Application Framework
|       |                           serverless.com, v1.67.3
 -------'

Serverless: Successfully generated boilerplate for template: "aws-python3"
```

### 模板配置

修改serverless.yml，指定AWS上部署的一些配置细节，包括部署的区域，命令行使用的profile等。如果不修改模板文件，也可以在部署时通过命令行参数提供。


```yaml
provider:
  name: aws
  runtime: python3.8
  # Lambda部署的AWS区域
  region: cn-northwest-1
  # AWS CLI Profile
  profile: cnlab
```

```yaml
functions:
  hello:
    handler: handler.hello
    # 在API Gateway中配置 HTTP API 来触发Lambda
    events:
      - httpApi: 'GET /'
```


修改handler.py：

```python
import json
def hello(event, context):
    body = {
        "message": "Hello World AWS Serverless"
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
```

### 部署与调试

接下来就可以进行部署：

```console
$ sls deploy
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
........
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service sls-lambda-python3.zip file to S3 (390 B)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
..............................
Serverless: Stack update finished...
Service Information
service: sls-lambda-python3
stage: dev
region: cn-northwest-1
stack: sls-lambda-python3-dev
resources: 11
api keys:
  None
endpoints:
  GET - https://9ea7dptou3.execute-api.cn-northwest-1.amazonaws.com.cn/
functions:
  hello: sls-lambda-python3-dev-hello
layers:
  None
Serverless: Run the "serverless" command to setup monitoring, troubleshooting and testing.
```

可以看到lambda已经部署到AWS上，同时配置了API Gateway HTTP API，接下来可以测试一下这个接口：

```console
$ curl https://9ea7dptou3.execute-api.cn-northwest-1.amazonaws.com.cn/
{"message": "Hello World AWS Serverless"}%   
```

查看Lambda执行的日志：

```console
$ sls logs -f hello 
START RequestId: 11a21905-0c6b-453d-8386-6367e99494fa Version: $LATEST
Debug:  {'message': 'Hello World AWS Serverless'}
END RequestId: 11a21905-0c6b-453d-8386-6367e99494fa
REPORT RequestId: 11a21905-0c6b-453d-8386-6367e99494fa  Duration: 1.34 ms       Billed Duration: 100 ms       Memory Size: 1024 MB    Max Memory Used: 53 MB  Init Duration: 697.87 ms
```

修改代码中变量body的值，并在本地进行运行查看结果：

```console
$ sls invoke local -f hello
Debug:  
{'message': 'Hello World AWS Serverless V2'}

{
    "statusCode": 200,
    "body": "{\"message\": \"Hello World AWS Serverless V2\"}"
}
```

可以看到本地运行结果已经更新，这时候使用 `sls deploy` 命令重新可以部署到云上并查看到返回结果已经更新。

### 使用 serverless-offline 插件进行本地调试

接下来我们尝试搭建本地的API Gateway + Lambda 的调试环境，需要安装Serverless Framework的一个插件： serverless-offline

```console
$ sls plugin install --name serverless-offline
Serverless: Creating an empty package.json file in your service directory
Serverless: Installing plugin "serverless-offline@latest" (this might take a few seconds...)
Serverless: Successfully installed "serverless-offline@latest"
```

该命令会自动修改 `serverless.yml` 文件以启用这个插件
```yaml
plugins:
  - serverless-offline
```
接着通过如下命令启用本地调试

```console
$ sls offline
offline: Starting Offline: dev/cn-northwest-1.
offline: Offline [http for lambda] listening on http://localhost:3002

   ┌─────────────────────────────────────────────────────────────────────────┐
   │                                                                         │
   │   GET | http://localhost:3000/dev                                       │
   │   POST | http://localhost:3000/2015-03-31/functions/hello/invocations   │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘

offline: [HTTP] server ready: http://localhost:3000 🚀
offline: 
offline: Enter "rp" to replay the last request
```

查看本地运行的结果：
```console
$ curl http://localhost:3000/dev
{"message": "Hello World AWS Serverless V2"}%
```

同时可以看到`sls offline`也会实时显示相关的日志:

```console
offline: GET /dev (λ: hello)
Debug:  {'message': 'Hello World AWS Serverless V2'}
offline: (λ: hello) RequestId: ck93gtjk40008ebs5dikdcq2m  Duration: 359.61 ms  Billed Duration: 400 ms
```

---