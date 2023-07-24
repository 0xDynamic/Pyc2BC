import sys, time, struct, marshal, dis, os, colorama, hashlib


def banner():
    print(
        f"""{colorama.Fore.MAGENTA}
                            _________________________________________________
                                ____                  __      ____       __  
                                /    )              /    )    /   )    /    )
                            ---/____/----------__----___/----/__ /----/------
                              /        /   / /   ' /        /    )   /       
                            _/________(___/_(___ _/____/___/____/___(____/___
                                         /                                   
                                     (_ /            
                                                             
                            Author: ChinoTheGod
                            Github: https://github.com/0xDynamic
                            > If there's a problem please create an issue on github
    """
    )


def error_banner():
    print(
        f"""{colorama.Fore.LIGHTRED_EX}
[-] Help: 
       -> Console disassembled Output: python pyc2bc.py -p <pyc_file_path>
       -> Save disassembled Output: python pyc2bc.py -p <pyc_file_path> -o <output_file_path>{colorama.Fore.RESET}
                        """
    )


MAGIC_TAG = {  # Updated magic number for lastest 3.11 version
    # Python 1
    20121: (1, 5),
    50428: (1, 6),
    # Python 2
    50823: (2, 0),
    60202: (2, 1),
    60717: (2, 2),
    62011: (2, 3),  # a0
    62021: (2, 3),  # a0
    62041: (2, 4),  # a0
    62051: (2, 4),  # a3
    62061: (2, 4),  # b1
    62071: (2, 5),  # a0
    62081: (2, 5),  # a0
    62091: (2, 5),  # a0
    62092: (2, 5),  # a0
    62101: (2, 5),  # b3
    62111: (2, 5),  # b3
    62121: (2, 5),  # c1
    62131: (2, 5),  # c2
    62151: (2, 6),  # a0
    62161: (2, 6),  # a1
    62171: (2, 7),  # a0
    62181: (2, 7),  # a0
    62191: (2, 7),  # a0
    62201: (2, 7),  # a0
    62211: (2, 7),  # a0
    # Python 3
    3000: (3, 0),
    3010: (3, 0),
    3020: (3, 0),
    3030: (3, 0),
    3040: (3, 0),
    3050: (3, 0),
    3060: (3, 0),
    3061: (3, 0),
    3071: (3, 0),
    3081: (3, 0),
    3091: (3, 0),
    3101: (3, 0),
    3103: (3, 0),
    3111: (3, 0),  # a4
    3131: (3, 0),  # a5
    # Python 3.1
    3141: (3, 1),  # a0
    3151: (3, 1),  # a0
    # Python 3.2
    3160: (3, 2),  # a0
    3170: (3, 2),  # a1
    3180: (3, 2),  # a2
    # Python 3.3
    3190: (3, 3),  # a0
    3200: (3, 3),  # a0
    3210: (3, 3),  # a1
    3220: (3, 3),  # a1
    3230: (3, 3),  # a4
    # Python 3.4
    3250: (3, 4),  # a1
    3260: (3, 4),  # a1
    3270: (3, 4),  # a1
    3280: (3, 4),  # a1
    3290: (3, 4),  # a4
    3300: (3, 4),  # a4
    3310: (3, 4),  # rc2
    # Python 3.5
    3320: (3, 5),  # a0
    3330: (3, 5),  # b1
    3340: (3, 5),  # b2
    3350: (3, 5),  # b2
    3351: (3, 5),  # 3.5.2
    # Python 3.6
    3360: (3, 6),  # a0
    3361: (3, 6),  # a0
    3370: (3, 6),  # a1
    3371: (3, 6),  # a1
    3372: (3, 6),  # a1
    3373: (3, 6),  # b1
    3375: (3, 6),  # b1
    3376: (3, 6),  # b1
    3377: (3, 6),  # b1
    3378: (3, 6),  # b2
    3379: (3, 6),  # rc1
    # Python 3.7
    3390: (3, 7),  # a1
    3391: (3, 7),  # a2
    3392: (3, 7),  # a4
    3393: (3, 7),  # b1
    3394: (3, 7),  # b5
    # Python 3.8
    3400: (3, 8),  # a1
    3401: (3, 8),  # a1
    3411: (3, 8),  # b2
    3412: (3, 8),  # b2
    3413: (3, 8),  # b4
    # Python 3.9
    3420: (3, 9),  # a0
    3421: (3, 9),  # a0
    3422: (3, 9),  # a0
    3423: (3, 9),  # a2
    3424: (3, 9),  # a2
    3425: (3, 9),  # a2
    # Python 3.10
    3430: (3, 10),  # a1
    3431: (3, 10),  # a1
    3432: (3, 10),  # a2
    3433: (3, 10),  # a2
    3434: (3, 10),  # a6
    3435: (3, 10),  # a7
    3436: (3, 10),  # b1
    3437: (3, 10),  # b1
    3438: (3, 10),  # b1
    3439: (3, 10),  # b1
    # Python 3.11
    3450: (3, 11),  # a1
    3451: (3, 11),  # a1
    3452: (3, 11),  # a1
    3453: (3, 11),  # a1
    3454: (3, 11),  # a1
    3455: (3, 11),  # a1
    3456: (3, 11),  # a1
    3457: (3, 11),  # a1
    3458: (3, 11),  # a1
    3459: (3, 11),  # a1
    3460: (3, 11),  # a1
    3461: (3, 11),  # a1
    3462: (3, 11),  # a2
    3463: (3, 11),  # a3
    3464: (3, 11),  # a3
    3465: (3, 11),  # a3
    3466: (3, 11),  # a4
    3467: (3, 11),  # a4
    3468: (3, 11),  # a4
    3469: (3, 11),  # a4
    3470: (3, 11),  # a4
    3471: (3, 11),  # a4
    3472: (3, 11),  # a4
    3473: (3, 11),  # a4
    3474: (3, 11),  # a4
    3475: (3, 11),  # a5
    3476: (3, 11),  # a5
    3477: (3, 11),  # a5
    3478: (3, 11),  # a5
    3479: (3, 11),  # a5
    3480: (3, 11),  # a5
    3481: (3, 11),  # a5
    3482: (3, 11),  # a5
    3483: (3, 11),  # a5
    3484: (3, 11),  # a5
    3485: (3, 11),  # a5
    3486: (3, 11),  # a6
    3487: (3, 11),  # a6
    3488: (3, 11),  # a6
    3489: (3, 11),  # a6
    3490: (3, 11),  # a6
    3491: (3, 11),  # a6
    3492: (3, 11),  # a7
    3493: (3, 11),  # a7
    3494: (3, 11),  # a7
    3495: (3, 11),  # b4
}


def magic_to_version(magic):
    magic_decimal = struct.unpack("<H", magic)[
        0
    ]  # Converts the magic number into Little Endian Integer
    return MAGIC_TAG[magic_decimal]


def analyze_code_obj(code_obj):
    no_entry = "[*] No Value"
    print(
        f"{colorama.Fore.LIGHTGREEN_EX}\n---------------[DISASSEMBLED CODE ATTRIBUTES]-------------------\n{colorama.Fore.RESET}"
    )
    print("[+] File Name: " + str(code_obj.co_filename))
    print("[+] Arguments: " + str(code_obj.co_argcount))
    print("[+] Constant Strings: \n")
    if not code_obj.co_consts:
        print("                     -> " + str(no_entry))
    else:
        for val in code_obj.co_consts:
            print("                     -> " + str(val))
    print("\n[+] Code Object Name: " + str(code_obj.co_name))
    print("[+] Number of Local Variables: " + str(code_obj.co_nlocals))
    print("[+] Local Variables: \n")
    if not code_obj.co_names:
        print("                     -> " + str(no_entry))
    else:
        for var in code_obj.co_names:
            print("                     -> " + str(var))
    print("\n[+] Arguments & Local variable names: \n")
    if not code_obj.co_varnames:
        print("                     -> " + str(no_entry))
    else:
        for argu in code_obj.co_varnames:
            print("                     -> " + str(argu))
    print("\n[*] Note: Other Attributes can be added by editing the code if required")
    # print("Free Variable Names: " + str(code_obj.co_freevars))
    # print("Cell Variable Names: " + str(code_obj.co_cellvars))
    # print("ByteCode: " + code_obj.co_code.hex())
    # print("Stack Size: " + str(code_obj.co_stacksize))
    # print("LNoTab: " + str(code_obj.co_lnotab))
    # print("First Line Number: " + str(code_obj.co_firstlineno))
    # print("Flags: " + str(code_obj.co_flags))
    print(
        f"{colorama.Fore.LIGHTGREEN_EX}\n-------------------[DISASSEMBLED BYTECODE]----------------------\n\n{colorama.Fore.RESET}"
    )
    dis.dis(code_obj)
    print("\n\n----------------------------[END]-------------------------------\n\n")


def disassemble_pyc(pathofpyc):
    try:
        start_time = time.time()
        with open(pathofpyc, "rb") as f:
            print(
                f"{colorama.Fore.LIGHTGREEN_EX}\n---------------------[PARSED PYC HEADER]------------------------{colorama.Fore.RESET}"
            )
            magic_number = f.read(
                2
            )  # Magic Number - Depends on the Python version whilst compilation
            carriage_return = f.read(
                2
            )  # Carriage return - remains identical in every python version
            compiled_python_version = magic_to_version(
                magic_number
            )  # Convert magic number to Python Version
            major_version = compiled_python_version[0]
            minor_version = compiled_python_version[1]
            print(
                "\n[+] Compiled PYC Python Version: "
                + str(major_version)
                + "."
                + str(minor_version)
            )

            hasher = hashlib.sha256()  # Create hash object
            chunk = f.read(4096)  # Read the file in chunks to save memory
            while chunk:
                hasher.update(chunk)  # Update hash with the content of the chunk
                chunk = f.read(4096)
                break  # Break the loop to prevent EOFError

            print(
                "[+] Hex SIP-HASH: " + hasher.hexdigest()
            )  # Return the hexadecimal representation of the hash
            end_time = time.time()
            execution_time = end_time - start_time
            print("[+] Execution took:", execution_time, "seconds")

            load_marshalled_code_obj = marshal.load(f)
            analyze_code_obj(load_marshalled_code_obj)

    except IOError:
        print("\n[-] Error: Cant Open the PYC File")

    except ValueError:
        print(
            "\n[-] Error: Mismatched Python versions - System & PYC Compiled (The python version of this file is different with your system python version)"
        )

    except KeyError:
        print("\n[-] Error: Invalid Magic Number")


# Input .PYC file - [Main Function]

if __name__ == "__main__":
    try:
        banner()
        if sys.argv[1] == "-p":
            path_of_pyc_file = sys.argv[2]
            if not os.path.exists(path_of_pyc_file):
                print("\n[-] Invalid Path: File does not exists !")
                error_banner()
                sys.exit()

            try:
                if sys.argv[3] == "-o":
                    try:
                        path_of_output_file = sys.argv[4]
                        if not os.path.exists(path_of_output_file):
                            print("\n[-] Invalid Output Path or File Already Exists")
                            error_banner()
                            sys.exit()
                        print("\n[+] Processing Disassembled Output")
                        stdoutOrigin = sys.stdout
                        sys.stdout = open("disasm_pyc.txt", "w")
                        disassemble_pyc(path_of_pyc_file)
                        sys.stdout.close()
                        sys.stdout = stdoutOrigin
                        print(
                            "[+] Saved Disassembled Output: "
                            + path_of_output_file
                            + "\\disasm_pyc.txt"
                        )
                    except IndexError:
                        print("[-] Error: Output Path not provided")
                        error_banner()

            except IndexError:
                disassemble_pyc(path_of_pyc_file)

        else:
            print("\n[-] Invalid Command")
            error_banner()

    except IndexError:
        print("\n[-] Invalid Command")
        error_banner()
