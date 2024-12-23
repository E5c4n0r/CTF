题目描述：

I heard that LSB steganography is not only used in image steganography.

solution：

解压然后看到01.png，尝试了之后发现不和噪音相关，然后结合文件名01，想到读取像素并查看它们是否代表数据流中的单个位（例如黑色为 0 位，白色为 1 位），最后发现黑色为 0 ，白色为 1 ，写个解密脚本

```plain
from PIL import Image

def image_to_bits(image_file):
    img = Image.open(image_file).convert("1")  
    width, height = img.size
    bits = ""

    for y in range(height):
        for x in range(width):
            bits += '0' if img.getpixel((x, y)) == 0 else '1'  # 0为黑色，1为白色

    return bits

def bits_to_text(bits):
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:  # 处理不足8位的情况
            break
        text += chr(int(byte, 2))  
    return text

def decrypt_image_to_text(image_file, text_file):
    bits = image_to_bits(image_file)  # 从图像中提取二进制位串
    text = bits_to_text(bits)  # 将二进制位串转换为文本

    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(text)  

image_file_path = "01.png"
text_file_path = "test"

decrypt_image_to_text(image_file_path, text_file_path)
```

删点空字符，然后发现test文件反序后是 89504E47 开头，明显的png头，反序后转换为16进制数据，改为png后缀得到密码为：`!!SUp3RP422W0RD^/??.&&`，这就是 key.zip 的密码，然后010打开 key 文件发现前面有段编码，base64解密得到：`stl stl stl`，搜索发现 `STL（STereoLithography，立体光刻）是一种3D模型文件格式`，这里注意STL文件头格式为80个字节，无论什么内容都行，所以只需要删去编码部分即可，改下后缀拿到在线网站：https://www.3dpea.com/cn/view-STL-online 去打开下得到 key:sSeCre7KeY?!!@$

![img](https://cdn.nlark.com/yuque/0/2024/png/39254810/1733572548924-ad06ad8f-df89-4ea8-b977-b7d3f3e724c1.png)

以此key去xor下flag文件得到一个wav文件（审wp的时候发现有的佬直接用一个普通wav文件异或flag文件就直接拿到key了，tql），根据题目描述的提示找到文章：https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2-c76b1be719b3，解音频文件的lsb隐写，按照其脚本解密即可得到flag：D0g3xGC{U_4rE_4_WhI2_4t_Ste9An09r4pHY}