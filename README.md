![pytest](https://github.com/signatelab/signate-cli/workflows/pytest/badge.svg) [![PyPI version](https://badge.fury.io/py/signate.svg)](https://badge.fury.io/py/signate)

# **SIGNATE CLI**
[SIGNATE](https://signate.jp) の公式APIコマンドラインインターフェイス(以下：SIGNATE CLI)です。  
SIGNATEはData Science Competitionのご提供を始めとした、データサイエンティストの皆様のための統合プラットフォームです。

**※SIGNATE CLIの動作にはPython3.6 以降の環境が必要です。**  
※当CLIはβ版であり、予告なく変更させていただく可能性がございます。予めご了承ください。  
※SIGNATE CLIはMac OSおよびLinuxをサポートしております。

# **インストールと事前準備**

以下のコマンドでインストールをお願いいたします。

```
$ pip install signate
```

インストール後、以下の手順を実施ください。

 1. [SIGNATE](https://signate.jp) でアカウント登録  
 2. アカウント登録後、[アカウント設定](https://signate.jp/account_settings) 画面の "API Token" の "作成" をクリック  
 3. "新規作成" をクリックしてAPI Token(``signate.json``)を取得  
 4. ~/.signateを作成  
 ＊ ~/ はホームディレクトリを指します。ホームディレクトリ直下に .signate を作成してください。  
 ＊ . から始まるフォルダは隠しフォルダです。隠しフォルダを表示した状態でご確認ください。  
 5. 取得したAPI Tokenを ``~/.signate``直下に配置   
 ＊ SIGNATE CLI 上でも API Token は取得できます。詳しくは「利用方法」⑤をご参照ください。  
 ＊ SNS で会員登録した場合は[アカウント設定](https://signate.jp/account_settings) 画面でのみ API Token を取得可能です。

以下のコマンドでヘルプが表示されましたら利用準備完了です。

```
$ signate --help
```

``signate: command not found`` と表示される場合、環境変数$PATH のディレクトリ内にsignateが存在していることをご確認ください。``pip uninstall signate``コマンドで

 - signateコマンドがインストールされているディレクトリの確認
 - signateコマンドのアンインストール

が可能です。

# **利用方法**
SIGNATE CLIでは以下の機能が利用できます。

```bash
$ signate --help
Usage: signate [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download  Download the file of competition
  files     List file of competition
  list      List competition
  submit    Submit a result file to the competition
  token     Download the API Token

``` 

### **① 投稿可能なコンペティション一覧の取得**
```
$ signate list 
```
投稿可能なコンペティション一覧を表示します。

``` bash 
$ signate list 

competitionId  title             closing              prize        participants
-------------  ----------------  -------------------  ---------  --------------
   1           a-ai-competition  -                    $200,00               100
   2           b-ai-competition  2019-12-31           Knowledge              50
……
```

### **② コンペティションが提供するファイル一覧の取得**
```
$ signate files --competition-id=<competition-id> 
```
コンペティションが提供するファイルの一覧を表示します。
``` bash 
$ signate files --competition-id=1

  fileId  name               title              size  updated_at
--------  -----------------  --------------  -------  -------------------
       1  train.csv          学習用データ      2345067  2016-05-31 11:19:48
       2  test.csv           検証用データ      1523536
……
```

### **③ コンペティションが提供するファイルのダウンロード**
**こちらの機能をご利用の場合、コンペティションへの参加に同意いただく必要がございます(同意前の場合)。**  
詳しくは[補足 コンペティションへの同意](#コンペティションへの同意)をご確認ください。


```
$ signate download --competition-id=<competition-id> 
```
コンペティションが提供するファイルをダウンロードします。
デフォルトの場合カレントディレクトリにファイルがダウンロードされます。  
competition-idのみを指定した場合、該当コンペティションが提供するすべてのファイルがダウンロード対象となります。

``` bash
$ signate download --competition-id=1 
submit_sample.csv
100% [.................................................................] 205890 / 205890
test.csv
100% [.................................................................] 1523536 / 1523536
train.csv
100% [.................................................................] 2345067 / 2345067

Download completed.

```
以下のようにご指定いただくことで、ダウンロードするファイルの指定とダウンロード先のパス指定もそれぞれ可能です。
``` bash
$ signate download --competition-id=1 --file-id=1 --path=/Users/[user_name]/Desktop/
train.csv
100% [.................................................................] 2345067 / 2345067

Download completed.

```

### **④ データセットの提出**
**こちらの機能をご利用の場合、コンペティションへの参加に同意いただく必要がございます(同意前の場合)。**  
詳しくは[補足 コンペティションへの同意](#コンペティションへの同意)をご確認ください。

``` bash 
signate submit --competition-id=<competition-id> <結果ファイルのパス>
``` 
コンペティションにデータセットを提出します。

```bash
$ signate submit --competition-id=1 /Users/[user_name]/Desktop/result.csv
You have successfully submitted your predictions. We will send you the submission result to your email address.
```
コメントを残すことも可能です。
```bash
$ signate submit --competition-id=1 /Users/[user_name]/Desktop/result.csv --note 頑張りました
You have successfully submitted your predictions. We will send you the submission result to your email address.
```


### **⑤ APITokenの取得**
APIトークン取得コマンドを実行し、APIでアクセスに必要なトークンを取得します。
``` bash
$ signate token --email=事前準備で登録したemail --password=事前準備で登録したパスワード
The Api Token successfully downloaded.
```


### **補足**
#### コンペティションへの同意
以下のようなメッセージが出力された際は
```
You have not accepted the competition terms of use!

Do you accept the competition terms of use?
Please read the terms of use before accepting: https://signate.jp/competitions/*#terms
 [y/N]:
```
リンク先をご一読いただき、``y`` のご入力をお願いいたします。以降、同一コンペティションで当メッセージは表示されません。
#### プロフィール入力の不足
```
You have not filled in user infomation to join the competition. Go to https://signate.jp/profile.
```
のメッセージが表示された場合は[SIGNATE](https://signate.jp)にアクセスいただき、プロフィールのご入力をお願いいたします。

# **ライセンス**
SIGNATE CLIは[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0). を適用しております。
