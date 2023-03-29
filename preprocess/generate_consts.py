import sys
import platform
import subprocess

CONST_FILE = "curl_cffi/const.py"
CURL_VERSION = sys.argv[1]

uname = platform.uname()


print("extract consts from curl.h")
with open(CONST_FILE, "w") as f:
    f.write("# This file is automatically generated, do not modify it directly.\n\n")
    f.write("from enum import IntEnum\n\n\n")
    f.write("class CurlOpt(IntEnum):\n")
    cmd = rf"""
        echo '#include "{CURL_VERSION}/include/curl/curl.h"' | gcc -E - | grep -i "CURLOPT_.\+ =" | sed "s/  CURLOPT_/    /g" | sed "s/,//g"
    """
    output = subprocess.check_output(cmd, shell=True)
    f.write(output.decode())
    f.write(
        """
    if locals().get("WRITEDATA"):
        FILE = locals().get("WRITEDATA")
    if locals().get("READDATA"):
        INFILE = locals().get("READDATA")
    if locals().get("HEADERDATA"):
        WRITEHEADER = locals().get("HEADERDATA")\n\n
"""
    )

    f.write("class CurlInfo(IntEnum):\n")
    cmd = rf"""
        echo '#include "{CURL_VERSION}/include/curl/curl.h"' | gcc -E - | grep -i "CURLINFO_.\+ =" | sed "s/  CURLINFO_/    /g" | sed "s/,//g"
    """
    output = subprocess.check_output(cmd, shell=True)
    f.write(output.decode())
    f.write(
        """
    if locals().get("RESPONSE_CODE"):
        HTTP_CODE = locals().get("RESPONSE_CODE")\n\n
"""
    )

    f.write("class CurlMOpt(IntEnum):\n")
    cmd = rf"""
        echo '#include "{CURL_VERSION}/include/curl/curl.h"' | gcc -E - | grep -i "CURLMOPT_.\+ =" | sed "s/  CURLMOPT_/    /g" | sed "s/,//g"
    """
    output = subprocess.check_output(cmd, shell=True)
    f.write(output.decode())
    f.write("\n")