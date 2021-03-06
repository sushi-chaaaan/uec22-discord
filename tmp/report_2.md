
# コンピュータリテラシレポート #02  

学籍番号:2210342  
氏名:鈴木謙太郎  
提出日付: 2022.04.18(月)  

```
await hogehoge()
```

# 演習2a

今回はブラジルの25%の電力を供給していると言われている  
イタイプ・ダム(ブラジルは世界有数の水力発電国家)の  
公式サイトにpingを行う。

```shell
sushi@sushiDAIV:~$ ping itaipu.gov.br
PING itaipu.gov.br (45.235.19.10) 56(84) bytes of data.
64 bytes from 45.235.19.10 (45.235.19.10): icmp_seq=1 ttl=225 time=333 ms
64 bytes from 45.235.19.10 (45.235.19.10): icmp_seq=2 ttl=225 time=370 ms
64 bytes from 45.235.19.10 (45.235.19.10): icmp_seq=3 ttl=225 time=337 ms
^C
--- itaipu.gov.br ping statistics ---
4 packets transmitted, 3 received, 25% packet loss, time 5604ms
rtt min/avg/max/mdev = 333.496/346.786/369.519/16.151 ms
```

さすが光の速さ、地球の裏側まででも概ね400ms以内に  
応答が帰ってきている。

今回は追加でtracerouteも行う。

```shell
sushi@sushiDAIV:~$ traceroute www.itaipu.gov.br
traceroute to www.itaipu.gov.br (45.235.19.10), 30 hops max, 60 byte packets
 1  sushiDAIV (192.168.128.1)  0.249 ms  0.211 ms  0.205 ms
 2  172.20.10.1 (172.20.10.1)  9.616 ms  9.610 ms  9.605 ms
 3  * * *
 4  * * *
 5  softbank126240058050.bbtec.net (126.240.58.50)  51.081 ms  51.071 ms  51.060 ms
 6  softbank126240058036.bbtec.net (126.240.58.36)  50.937 ms  37.959 ms  37.918 ms
 7  softbank126240058041.bbtec.net (126.240.58.41)  37.894 ms  39.932 ms  39.909 ms
 8  softbank221110214177.bbtec.net (221.110.214.177)  39.867 ms  39.860 ms  39.854 ms
 9  * * *
10  * * *
11  softbank221111203074.bbtec.net (221.111.203.74)  145.604 ms  145.595 ms  137.980 ms
12  ae10.cs2.lax112.us.eth.zayo.com (64.125.27.234)  206.859 ms  196.267 ms  222.036 ms
13  ae21.mpr1.slc2.us.zip.zayo.com (64.125.26.19)  168.532 ms  157.452 ms  168.510 ms
14  ae4.mpr2.slc2.us.zip.zayo.com (64.125.26.165)  168.489 ms  168.449 ms  168.439 ms
15  * ae11.cs1.den5.us.zip.zayo.com (64.125.26.42)  184.792 ms  192.248 ms
16  * * *
17  * * *
18  * * *
19  208.185.175.78.IDIA-310002-002-ZYO.zip.zayo.com (208.185.175.78)  196.653 ms  268.703 ms  268.691 ms
20  globenet-227.as52320.net (200.16.71.227)  185.482 ms  268.689 ms  268.681 ms
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  177.3.184.106 (177.3.184.106)  469.401 ms  469.398 ms  469.394 ms
30  * * *
```

少々長くなってしまったが、スマートフォンのテザリングを使用して行ったため、  
途中まではSoftBankのサーバーを経由している。  
その後、どうやら日本の外にあるらしいSoftBankのサーバー(11)を経由して、  
アメリカにある光ファイバー企業のサーバーを経由してブラジルまで接続しているようだ。  
地球全域をカバーするネットワークが大きいことは理解していたが、  
経由するサーバーの数が30近いのを見るとその規模を改めて実感する。

# 演習2b

ここでは、世界各地でサービスを展開するAmazonの各国のサイトへpingを  
送信することで世界の複数地域までのパケットの往復時間を調べる。

## 各リージョンにpingした結果

```shell
[JAPAN]
sushi@DESKTOP-IVPQOIS:~$ ping amazon.co.jp
PING amazon.co.jp (52.119.164.121) 56(84) bytes of data.
64 bytes from 52.119.164.121 (52.119.164.121): icmp_seq=1 ttl=232 time=127 ms
```

```shell
[AMERICA]
sushi@DESKTOP-IVPQOIS:~$ ping amazon.com
PING amazon.com (54.239.28.85) 56(84) bytes of data.
64 bytes from 54.239.28.85 (54.239.28.85): icmp_seq=1 ttl=226 time=169 ms
```

```shell
[BRAZIL]
sushi@DESKTOP-IVPQOIS:~$ ping amazon.com.br
PING amazon.com.br (54.239.26.87) 56(84) bytes of data.
64 bytes from 54.239.26.87 (54.239.26.87): icmp_seq=1 ttl=228 time=171 ms
```

```shell
[NETHERLAND]
sushi@DESKTOP-IVPQOIS:~$ ping amazon.nl
PING amazon.nl (52.95.120.64) 56(84) bytes of data.
64 bytes from 52.95.120.64 (52.95.120.64): icmp_seq=1 ttl=223 time=251 ms
```

## 考察

驚いたのは、北米のAmazonとブラジルのAmazonへの所要到達時間がほぼ同じであることである。  
tracerouteを使ったところ、両者の経路はまったく異なっていたので、太平洋にケーブルが敷かれているのだろう。  
また、距離的にはブラジルより近いはずのオランダのAmazonの方が、到達時間が長いので  
ヨーロッパ方面へのネットワークは存外不便なのかもしれない。  

実際に[世界のインターネットの大まかな配置](https://www.submarinecablemap.com/)を見てみると、ヨーロッパ方面へのアクセスはかなり遠回りをしているように見えるため、  
結果的に物理的はより近いのに、pingに要する時間が長いという逆転現象が起きていると思われる。  

# 演習2c

[演習2b](#演習2b)は、当初世界各国のGoogleにアクセスしてpingを測定する予定だった。  
しかしながら、下のコードブロックのように、

```shell
[JAPAN]
sushi@DESKTOP-IVPQOIS:~$ ping google.co.jp
PING google.co.jp (172.217.161.35) 56(84) bytes of data.
64 bytes from nrt12s23-in-f3.1e100.net (172.217.161.35): icmp_seq=1 ttl=114 time=3.25 ms
```

```shell
[BRAZIL]
sushi@DESKTOP-IVPQOIS:~$ ping google.com.br
PING google.com.br (172.217.175.99) 56(84) bytes of data.
64 bytes from nrt20s21-in-f3.1e100.net (172.217.175.99): icmp_seq=1 ttl=112 time=4.96 ms
```

日本のGoogleとブラジルのGoogleの両方にpingを送った結果、ほぼ同じ結果だった。  
tracerouteを使ったところ、両者のたどるIPアドレスが末尾のみ違う、のような状態なので、  
おそらくGoogleなどの非常にトラフィックが多いサイトはCDNを使っていて、  
日本のキャッシュサーバーにキャッシュが乗っているものと考えられる。

# 演習4

演習2で複数回tracerouteを実行しているので省略する。

# 演習4a

```shell
[GOOGLE]
sushi@DESKTOP-IVPQOIS:~$ traceroute google.co.jp
traceroute to google.co.jp (172.217.161.35), 30 hops max, 60 byte packets
 1  DESKTOP-IVPQOIS (172.29.16.1)  0.133 ms  0.117 ms  0.112 ms
 2  RT-AX56U-FF98 (192.168.50.1)  0.600 ms  0.399 ms  1.329 ms
 3  172.16.64.1 (172.16.64.1)  1.764 ms  1.870 ms  1.866 ms
 4  10.0.0.5 (10.0.0.5)  1.865 ms  1.943 ms  1.939 ms
 5  192.168.33.5 (192.168.33.5)  3.845 ms  3.271 ms  3.778 ms
 6  tmfACS001.bb.kddi.ne.jp (27.85.212.65)  5.405 ms tmfACS001.bb.kddi.ne.jp (27.85.212.129)  3.759 ms tmfACS001.bb.kddi.ne.jp (27.85.212.65)  4.082 ms
 7  27.80.241.173 (27.80.241.173)  4.654 ms  3.493 ms  8.224 ms
 8  27.85.137.90 (27.85.137.90)  3.474 ms 27.86.120.218 (27.86.120.218)  3.473 ms 27.86.45.6 (27.86.45.6)  3.691 ms
 9  72.14.242.21 (72.14.242.21)  3.892 ms  3.888 ms  4.080 ms
10  * * *
11  142.250.226.58 (142.250.226.58)  4.529 ms 108.170.242.193 (108.170.242.193)  8.177 ms  5.413 ms
12  108.170.242.209 (108.170.242.209)  5.296 ms 108.170.242.176 (108.170.242.176)  4.966 ms 108.170.242.177 (108.170.242.177)  3.651 ms
13  209.85.246.83 (209.85.246.83)  3.980 ms nrt12s23-in-f3.1e100.net (172.217.161.35)  3.913 ms  3.621 ms
```

```shell
[KANTEI]
sushi@DESKTOP-IVPQOIS:~$ traceroute kantei.go.jp
traceroute to kantei.go.jp (13.249.150.75), 30 hops max, 60 byte packets
 1  DESKTOP-IVPQOIS (172.29.16.1)  0.142 ms  0.126 ms  0.120 ms
 2  RT-AX56U-FF98 (192.168.50.1)  0.433 ms  0.429 ms  0.976 ms
 3  172.16.64.1 (172.16.64.1)  2.092 ms  2.185 ms  2.002 ms
 4  10.0.0.5 (10.0.0.5)  1.947 ms  2.074 ms  2.166 ms
 5  192.168.33.5 (192.168.33.5)  3.687 ms  3.681 ms  3.710 ms
 6  tmfACS001.bb.kddi.ne.jp (27.85.212.129)  4.606 ms tmfACS001.bb.kddi.ne.jp (27.85.212.65)  8.173 ms  8.158 ms
 7  106.139.194.29 (106.139.194.29)  17.689 ms 27.80.241.69 (27.80.241.69)  11.013 ms 106.139.194.21 (106.139.194.21)  10.971 ms
 8  27.86.41.102 (27.86.41.102)  10.486 ms 27.85.228.22 (27.85.228.22)  10.481 ms  10.867 ms
 9  175.129.54.50 (175.129.54.50)  11.080 ms  11.116 ms  11.071 ms
10  15.230.24.180 (15.230.24.180)  12.239 ms  12.154 ms 15.230.24.248 (15.230.24.248)  10.962 ms
11  15.230.25.37 (15.230.25.37)  10.492 ms 15.230.24.93 (15.230.24.93)  10.710 ms 15.230.24.129 (15.230.24.129)  18.283 ms
12  * * *
13  150.222.91.40 (150.222.91.40)  10.681 ms 54.239.53.70 (54.239.53.70)  19.155 ms 150.222.91.24 (150.222.91.24)  10.774 ms
14  52.93.150.9 (52.93.150.9)  9.558 ms 52.93.150.7 (52.93.150.7)  10.623 ms  10.721 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  server-13-249-150-75.nrt51.r.cloudfront.net (13.249.150.75)  12.276 ms  11.188 ms  11.308 ms
```

上はgoogle.co.jpへのtracerouteで、下は[首相官邸ホームページ](https://www.kantei.go.jp/)へのtracerouteの結果である。  
途中の六個目のサーバーまではまったく同じものを経由しているので、おそらく日本国内のネットワークの  
集権的なサーバーをKDDIが運用しているのだろう。

# 演習4b

```shell
sushi@DESKTOP-IVPQOIS:~$ traceroute www.itaipu.gov.br
traceroute to www.itaipu.gov.br (45.235.19.10), 30 hops max, 60 byte packets
 1  DESKTOP-IVPQOIS (172.29.16.1)  0.184 ms  0.168 ms  0.162 ms
 2  RT-AX56U-FF98 (192.168.50.1)  1.304 ms  1.465 ms  0.827 ms
 3  172.16.64.1 (172.16.64.1)  1.847 ms  1.755 ms  1.949 ms
 4  10.0.0.5 (10.0.0.5)  1.837 ms  1.939 ms  1.935 ms
 5  192.168.33.5 (192.168.33.5)  4.196 ms  4.152 ms  3.710 ms
 6  tmfACS001.bb.kddi.ne.jp (27.85.212.129)  5.821 ms tmfACS001.bb.kddi.ne.jp (27.85.212.65)  8.309 ms  8.294 ms
 7  27.80.241.173 (27.80.241.173)  8.289 ms 106.139.194.85 (106.139.194.85)  6.286 ms 27.80.241.157 (27.80.241.157)  5.959 ms
 8  106.187.12.14 (106.187.12.14)  114.009 ms 106.187.12.38 (106.187.12.38)  110.306 ms 106.187.12.14 (106.187.12.14)  114.002 ms
 9  203.181.106.170 (203.181.106.170)  114.066 ms  114.170 ms  114.041 ms
10  124.215.192.134 (124.215.192.134)  113.106 ms  110.691 ms  113.142 ms
11  ae1.sanpaolo1.spa.seabone.net (195.22.219.155)  258.152 ms  253.886 ms  276.286 ms
12  acessoline.sanpaolo1.spa.seabone.net (149.3.181.51)  269.526 ms  269.901 ms  272.068 ms
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

これは、[演習2a](#演習2a)で、SoftBank回線のテザリングを経由してtracebackを十個スチアブラジルのダムに、  
自宅の回線からtracerouteを実行した結果である。見比べたところ、まったく違うものを経由している。  

# 演習4c

# 演習5

私は自分で`sushichan.live` というドメインを取得している。  
今現在は外部向けにサービスを公開していないが、以前はゲームサーバー  
などを外部に公開していた。  
このドメインは現在CloudFlareのレジストラで取得されている。  
維持費は$17.68/年となっている。  
