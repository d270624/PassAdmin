from Crypto.Cipher import AES
import base64


class RsaChange:
    def __init__(self):
        self.key = "MIICXwIBAAKBgQCT1c0FdB81pqSgpUgA"

    # str不是16的倍数那就补足为16的倍数
    def add_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    # 加密方法
    def encryption(self, message):
        # 秘钥
        # 待加密文本
        # 初始化加密器
        try:
            aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)
            # 先进行aes加密
            encrypt_aes = aes.encrypt(self.add_to_16(message))
            # 用base64转成字符串形式
            encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
            return encrypted_text
        except:
            pass

    # 解密方法
    def decrypt(self, text):
        # 秘钥
        # 密文
        # 初始化加密器
        try:
            aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)
            # 优先逆向解密base64成bytes
            base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
            # 执行解密密并转码返回str
            decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
            return decrypted_text
        except:
            pass

    def generate(self):  # 生成密钥
        pass
        # 生成密钥
        # (pubkey, privkey) = rsa.newkeys(1024)

        # 保存密钥
        # with open('public.pem', 'w+') as f:
        #     f.write(pubkey.save_pkcs1().decode())
        #
        # with open('private.pem', 'w+') as f:
        #     f.write(privkey.save_pkcs1().decode())
