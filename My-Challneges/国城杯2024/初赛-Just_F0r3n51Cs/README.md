谷歌网盘附件下载：https://drive.google.com/file/d/13qDiA1_lKko-Nlb6quFuh_nxMceP-c44/view?usp=sharing（压缩包解压密码：Rca@(@b2&b-9^6de*32(A，附件MD5值为：0f3df40c8ec0599e2f88fdd5a81023f2）

题目描述：

flag被分为4份藏在了这台计算机中，从哪入手呢？先从beginning开始吧

solution：

开题是一个E01，我这里用的是autopsy来取证，首先看到桌面有个流量包，对应题目描述beginning，应该是flag1

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572635888-ebf5d181-2e15-4e89-bf45-1251997968cb.png)

提取出来，打开发现有tcp等多种协议，还有oicq协议，就是QQ的协议，先提取出一个jpg，010查看其文件尾发现有多余数据，先是一串base64，然后是一串加密的数据，先base64解码后得到`oursecret is D0g3xGC`，猜测加密的数据是oursecret隐写了，用 D0g3xGC 解密得到hidden.txt，内容是

```plain
ECB's key is
N11c3TrYY6666111
记得给我秋秋空间点赞
```

提示说看QQ空间，看一下oicq协议中的QQ号

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572659967-0fd3bd60-09fe-497d-baef-cfdb2342023a.png)

然后看到QQ空间第一条说说最后面的密文

![img](https://cdn.nlark.com/yuque/0/2024/jpeg/39254810/1733572679016-e185408c-35db-4a3e-b47b-4aa4950b4152.jpeg)

```plain
5e19e708fa1a2c98d19b1a92ebe9c790d85d76d96a6f32ec81c59417595b73ad
```

然后拿去解密得到flag1：`D0g3xGC{Y0u_`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572710162-28912100-799e-4268-a868-7f43e98984af.png)查看环境变量，注册表下看，注册表在`C:\Windows\System32\config`目录下，查看`SYSTEM\CurrentControlSet001\Control\Session Manager\Environment`的键值对，发现`u_can_get_flag2_here`的值为一个文件

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572759795-d65e9635-915a-431b-928a-80507d4ee296.png)

据此找到flag2的位置，可以看到是个zip，提取出来 

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572778120-e24f2e39-2936-42a4-9f1d-4f3c02f9d6de.png)

改下后缀然后打开可以看到注释

```plain
1、计算机注册时设置的用户名（答案格式：Bo6）
2、计算机当前操作系统的产品名称，若有空格则用下划线代替（答案格式：Windows_Server_2016）
3、计算机当前安装的 Mozilla Firefox 浏览器的版本号，保留一位小数（答案格式：91.0）
最终压缩包密码格式：B06_Windows_Server_2016_91.0
```

注册表取证，注册表文件在`C:\Windows\System32\Config`目录下

第一个答案是注册表HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion中的 RegisteredOwner 的键值`D0g3xGC`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572805922-ad37b942-677f-44a6-bd31-6f842d543e16.png)

第二个答案是注册表HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion中的 ProductName 的键值 `Windows_7_Ultimate`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572827113-bef3007c-9f72-49a4-84ec-0e219b83bada.png)

第三个答案是注册表HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Mozilla Firefox中的CurrentVersion的值 `115.0`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572847931-c2b879be-cc8c-43fd-ad64-38bdeca1fc45.png)

故最终压缩包密码为`D0g3xGC_Windows_7_Ultimate_115.0`，得到密文

```plain
#@~^HAAAAA==W^lLyPb/P@#@&4*.2{W!!x[mFC&|0AcAAA==^#~@ 
```

是vbe的格式，改下后缀拿到：https://master.ayra.ch/vbs/vbs.aspx，解密得到flag2

```plain
flag2 is 
h4V3_f0und_7H3_
```

根据autopsy的自动分析，找到个加密的Original_is_here.zip

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572887310-5dd295a9-9664-4171-bc7a-c25d645bf7a3.png)

跟踪到其存在的目录下发现还有个png

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572902519-e6ad1082-90c7-4d74-bb50-397b45cd5ddd.png)

搜了一下CatWatermark，找到项目：https://github.com/Konano/CatWatermark，有加密和解密脚本，根据解密脚本所需参数猜测zip中是原图，666就是其三个私钥参数，将其都提取出来，发现zip注释中有

```plain
1、计算机用户D0g3xGC登录时的密码（答案格式：a123456+）
2、账号D0g3xGC@qq.com登录otterctf网站时的密码（答案格式：PA55word）
最终压缩包密码格式：a123456+_PA55word
```

第一个的做法是提取出（/Windows/System32/config）中的 SYSTEM 和 SAM 文件，再用mimikatz提取哈希

```plain
privilege::debug                             //进入特权模式
lsadump::sam /system:"E:\SYSTEM" /sam:"E:\SAM"
```

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573012662-bd5decc0-7959-487a-acfd-a59852f2d6ca.png)

直接拿到 https://www.cmd5.com/ 去解密得到`qwe123!@#`

第二个是火狐的一个取证（结果发现貌似axiom能直接梭），要找到key4.db和login.json，可以在`C:\Users\D0g3xGA\AppData\Roaming\Mozilla\Firefox\Profiles\414u1hob.default-release`目录下找到，提取出来再用firewd解密即可

```plain
python firepwd.py logins.json
```

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573045310-79bc987f-2a8a-4e72-bc01-0f631601c846.png)

故压缩包密码为`qwe123!@#_Y0u_f1Nd^_^m3_233`，得到 Original.png 后就可以直接用项目的解密脚本解密了

```plain
python decode.py Original.png CatWatermark_666.png extracted_watermark.png 6 6 6
```

得到flag3：`F1N4L_s3CR3t_0F_Th15_`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573062569-78f3c977-26f0-4728-88d8-01e3df90676d.png)

在当前用户的目录下可以看到有个flag4.zip

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573163074-460cded1-36a3-420c-9fc9-7e67ae677ccf.png)

提取出来后发现这个是一个py打包成的exe，直接用 [pyinstxtractor-ng.exe](https://github.com/pyinstxtractor/pyinstxtractor-ng/releases/download/2024.08.25/pyinstxtractor-ng.exe) 解包出pyc文件再去反编译这个pyc文件就可以看的python代码了

所以先pyinstxtractor-ng.exe解包这个exe，找到enc_png.pyc文件，用在线pyc反编译网站反编译这个pyc文件得到python代码：

[在线Python pyc文件编译与反编译](https://www.lddgo.net/string/pyc-compile-decompile)（因为这个题目的python版本低，所以用uncompyle6反编译的效果好一点）

```plain
# uncompyle6 version 3.9.1
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.6.12 (default, Feb  9 2021, 09:19:15) 
# [GCC 8.3.0]
# Embedded file name: enc_png.py


def xor_encrypt(data, key):
    encrypted_data = bytearray()
    for i in range(len(data)):
        encrypted_data.append(data[i] ^ key[i % len(key)])
    else:
        return encrypted_data


def read_file(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    return data


def write_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)


def encrypt_file(input_file_path, output_file_path, key):
    data = read_file(input_file_path)
    encrypted_data = xor_encrypt(data, key)
    write_file(output_file_path, encrypted_data)


if __name__ == "__main__":
    key = b'GCcup_wAngwaNg!!'
    input_file = "flag4.png"
    encrypted_file = "flag4_encrypted.bin"
    encrypt_file(input_file, encrypted_file, key)
```

得到这个bin文件加密的代码，看代码可知，就只是对这个png文件进行了一个循环异或，异或的key也直接给出了，所以直接写脚本对这个文件异或回去就可以了（注意修改自己的bin文件路径）：

```plain
import os

def xor_encrypt(data, key):
    decrypted_data = bytearray()
    for i in range(len(data)):
        decrypted_data.append(data[i] ^ key[i % len(key)])
    return decrypted_data

def read_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    return data

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

def decrypt_file(input_file_path, output_file_path, key):
    data = read_file(input_file_path)
    decrypted_data = xor_encrypt(data, key)
    write_file(output_file_path, decrypted_data)

if __name__ == '__main__':
    key = b'GCcup_wAngwaNg!!'
    encrypted_file = "flag4_encrypted.bin"
    decrypted_file = "flag4_decrypted.png"
    decrypt_file(encrypted_file, decrypted_file, key)
```

最后得到flag4：`F0R3N51c5_Ch4Ll3N93}`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573187102-73cd9016-a84f-4eb2-b258-ece758a1dda1.png)

最终flag：D0g3xGC{Y0u_h4V3_f0und_7H3_F1N4L_s3CR3t_0F_Th15F0R3N51c5_Ch4Ll3N93}