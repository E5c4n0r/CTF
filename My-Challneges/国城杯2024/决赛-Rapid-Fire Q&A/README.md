题目描述：

Guido van Rossum first released Python 0.9.0 in 1991[33]. Python 2.0 was released in 2000, introducing new features. Python 3.0, released in 2008, was a major revision of the language and not fully backward compatible.

hint：

1、题目环境是python2

2、whitelist = "~()<{}[]>./?"

3、构造2000即可

环境搭建

```
docker build -t pyjail .
docker run -d -p 12133:12133 pyjail
```

solution：

开题

```
Welcome to Rapid-fire Q&A! Answer the question, and you'll get the flag.
What year was Python 2 released?
Enter your answer:
```

根据题目描述知道python2是2000年发行的，答案是2000，输入却回显`Invalid character detected, not in whitelist!`。说明只能用白名单中的字符，手动或者脚本fuzz都行，最后可用字符为`~()<{}[]>./?`，参考文章：https://www.aloxaf.com/2018/08/tjctf_pythonjail/#%E6%88%91%E7%8C%9C%E6%83%B3%E7%9A%84%E6%A0%87%E5%87%86%E8%A7%A3%E6%B3%95，发现在Python2中利用 `[] < []` 可以得到 False, `{} < []` 可以得到 True，也就是0和1，这样再通过取反和位移就可以得到任意数字，在原文的脚本上稍做了点修改，方便命令行直接输入参数

```
import sys

def brainfuckize(nb):
    if nb in [-2, -1, 0, 1]:
        return ["~({}<[])", "~([]<[])", "([]<[])", "({}<[])"][nb + 2]

    if nb % 2:
        return "~%s" % brainfuckize(~nb)
    else:
        return "(%s<<({}<[]))" % brainfuckize(nb // 2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python2 test.py <number>")
        sys.exit(1)

    try:
        num = int(sys.argv[1])
        result = brainfuckize(num)
        print("Brainfuck representation of {}:".format(num))
        print(result)
    except ValueError:
        print("Invalid input. Please provide an integer.")
        sys.exit(1)
```

最后构造出2000

```
((((~(~(~((((~({}<[])<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))<<({}<[]))
```

后续 ：

白名单那里多给了几个字符是为了混淆一下，避免只给payload中的字符被一眼丁真秒了，结果比赛时间3h，我这也没提前声明是python2的环境，估计大家看了一点觉得有点谜语人，就去看其他题了，导致0解，我的锅，赛后 t1d 佬说用 `()~</` 就行了，发现还真是







