题目描述：

解密反转再解密

solution：

开题是一个java的图片，再结合题目名，猜测是java盲水印，直接用 https://github.com/ww23/BlindWatermark 解密

```
java -jar BlindWatermark.jar decode -c password.png decode.png
```

![decode](https://bu.dusays.com/2024/12/23/676915726162e.png)

得到密码`A7f#9xQ!r3b$T`，得到一个reverse.jpg和flag.txt，直接解密flag.txt解密不出，猜测是有密钥的加密，结合文件名和题目描述反转，将reverse.jpg反色得到一个二维码，扫码得到

```
qwe：tewatnolzsarffuykjydyayd
```

猜测是qwe加密，脚本解密

```
def decrypt_qwe(s):
    DIC_QWE = "qwertyuiopasdfghjklzxcvbnm"
    DIC_ABC = "abcdefghijklmnopqrstuvwxyz"
    result=""
    for i in s:
        for j in range(len(DIC_ABC)):
            if i==DIC_QWE[j]:
                result=result+DIC_ABC[j]
    return result

s = "tewatnolzsarffuykjydyayd"

decrypted = decrypt_qwe(s)
print("解密结果:", decrypted)
```

解密得到：ecbkeyistlkdnngfrqfmfkfm，拿去解ecb即可

![image-20241212180951303](https://bu.dusays.com/2024/12/23/676915724c14e.png)

后续：

感觉挺简单的，不知道为啥只有一解，有个队伍盲水印解出来有点模糊，当时没看仔细，给他们说下个最新版的试试，然后他们貌似就一直在找最新版，结果后面想了下好像是版本下错了，他们下的是x86_64的，按理说直接下64的就行，不知道是不是这个原因





