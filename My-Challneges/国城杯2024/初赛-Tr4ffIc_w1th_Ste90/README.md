题目描述：

小p把他的秘密锁了起来，为了防止忘记密码，他记密码时用obs将这个过程录制了下来，然后用默认格式输出，但现在他忘了密码，也弄丢了视频，只剩下一个流量包，你能帮忙解密他的秘密吗？

solution：

打开流量包发现有很多UDP流，还可以发现传输格式是MPEG-TS，编码格式为H.264，说明传输的是ts流，题目描述中提到是obs录制的视频，obs录制的视频默认的输出方式为mkv，故思路就是提取出数据再转换为ts文件，最后将ts文件转换为mkv即可

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573208613-ee122828-66c4-4edc-b845-96be556616f8.png)

先从流量包中提取 UDP 流并保存为文件

```plain
tshark -r password.pcapng -Y "udp.port == 5555" -T fields -e data > udp_stream.txt
```

将提取的十六进制数据转换为二进制文件（网络传输的内容一般是以二进制流的形式存在，但为了便于保存和查看，`tshark`将其转化成了十六进制格式）：

```plain
import binascii

with open('udp_stream.txt', 'r') as f:
    hex_data = f.read().replace('\n', '')

bin_data = binascii.unhexlify(hex_data)

with open('extracted_video.ts', 'wb') as f:
    f.write(bin_data)
```

使用 `ffmpeg` 将提取的 TS 文件转换为 MKV 文件：

```plain
ffmpeg -i extracted_video.ts -c copy recovered.mkv
```

得到压缩包的密码 `!t15tH3^pAs5W#RD*f0RFL@9`

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573231987-47ddeb82-f575-419d-8a79-750b42cbd715.png)

解开challenge.zip后有个加密脚本和加密后的图片，加密脚本的大概作用就是用个随机数种子来打乱像素的行列位置，但不知道随机数的具体大小，脚本最后提示了`just 50 - 70`，写个脚本爆破一下即可

```plain
import numpy as np
import cv2
import os

def decode(input_image, output_image, seed):
    np.random.seed(seed)  
    to_hide = cv2.imread(input_image)
    
    if to_hide is None:
        print(f"Error: Unable to load image {input_image}")
        return
    
    to_hide_array = np.asarray(to_hide)
    shape = to_hide_array.shape

    row_indices = list(range(shape[0]))
    col_indices = list(range(shape[1]))

    np.random.shuffle(row_indices)
    np.random.shuffle(col_indices)

    inverse_row_indices = np.argsort(row_indices)
    inverse_col_indices = np.argsort(col_indices)

    to_hide_array = to_hide_array[inverse_row_indices, :]
    to_hide_array = to_hide_array[:, inverse_col_indices]

    cv2.imwrite(output_image, to_hide_array)
    print(f"Decoded image saved as {output_image}")

def brute_force_decode(input_image, output_folder, seed_range):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for seed in seed_range:
        output_image = os.path.join(output_folder, f"decoded_{seed}.png")
        decode(input_image, output_image, seed)

def main():
    input_image = "encoded.png"  
    output_folder = "decode"  
    seed_range = range(50, 71)  

    brute_force_decode(input_image, output_folder, seed_range)

if __name__ == '__main__':
    main()
```

最后发现seed为63的时候是个Data Matrix条码

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573285314-0500f056-c2fb-49d6-8aa4-00b819a5dc2e.png)

拿到在线网址：https://products.aspose.app/barcode/zh-hans/recognize/datamatrix# ，识别一下得到

```
I randomly found a word list to encrypt the flag. I only remember that Wikipedia said this word list is similar to the NATO phonetic alphabet.

crumpled chairlift freedom chisel island dashboard crucial kickoff crucial chairlift drifter classroom highchair cranky clamshell edict drainage fallout clamshell chatter chairlift goldfish chopper eyetooth endow chairlift edict eyetooth deadbolt fallout egghead chisel eyetooth cranky crucial deadbolt chatter chisel egghead chisel crumpled eyetooth clamshell deadbolt chatter chopper eyetooth classroom chairlift fallout drainage klaxon
```

提示说`我随机找到了一个单词列表来加密旗标（或信息），我只记得维基百科上说这个单词列表类似于北约音标字母。`，最终找到PGP词汇表

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733573302465-487c33ed-5874-43aa-ae28-bba3ab1c5658.png)

拿去在线网址解密：https://goto.pachanka.org/crypto/pgp-wordlist/，得到flag：D0g3xGC{C0N9rA7ULa710n5_Y0U_HaV3_ACH13V3D_7H15_90aL}